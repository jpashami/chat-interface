from flask import Flask, render_template, request, jsonify, Response
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    try:
        user_message = request.args.get('message', '')
        logger.debug(f"Received message: {user_message}")
        
        # Prepare the request to Ollama with length guidance in the prompt
        system_prompt = "Please provide clear and concise responses. While there's no strict word limit, aim to keep responses focused and well-structured. For code examples, include complete, working code with necessary context."
        full_prompt = f"{system_prompt}\n\nUser: {user_message}"
        
        ollama_data = {
            "model": "deepseek-r1:8b",
            "prompt": full_prompt,
            "stream": True
        }
        
        logger.debug(f"Sending request to Ollama: {json.dumps(ollama_data)}")
        
        def generate():
            # Send request to Ollama with streaming
            response = requests.post(OLLAMA_API_URL, json=ollama_data, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        if 'response' in json_response:
                            response_text = json_response['response']
                            
                            # Skip <think> tags
                            if response_text.startswith('<think>') or response_text == '</think>':
                                continue
                            
                            yield f"data: {json.dumps({'chunk': response_text})}\n\n"
                            logger.debug(f"Sent chunk: {response_text}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON: {str(e)}")
                        continue
            
            yield "data: [DONE]\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error communicating with Ollama: {str(e)}'
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 