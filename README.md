# Ollama Chat Interface

A Flask web application that provides a chat interface for communicating with Ollama AI models running locally.

## Prerequisites

- Python 3.7 or higher
- Ollama installed and running locally
- A model downloaded in Ollama (default is llama2)

## Setup

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is running locally on your machine.

3. Start the Flask application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Type your message in the input field at the bottom of the chat interface
2. Press Enter or click the Send button to send your message
3. Wait for the AI response
4. Continue the conversation as needed

## Customization

- To use a different Ollama model, modify the `model` parameter in the `chat` route in `app.py`
- The interface can be customized by modifying the CSS in `templates/index.html`

## Troubleshooting

If you encounter any issues:
1. Ensure Ollama is running locally
2. Check that the Ollama API is accessible at http://localhost:11434
3. Verify that you have a model downloaded in Ollama
4. Check the Flask application logs for any error messages 