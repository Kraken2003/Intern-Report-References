from flask import Flask, request, jsonify
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

app = Flask(__name__)

def get_gemini_response(question, image_data):
    
    system_prompt = """You are an excellent Invoice analyzer. 
    Your job is to read the invoice image provided to you correctly in the first try. 
    You have to be accruate with your readings. 
    You have to only give the output of the read data in a json format and nothing else. Make sure you include the units of the items etc.
    Also add spacing of newlines so the json response looks nice.
    If the data in invoice is in a different language other than english then translate it to english and put the translated response in the json data.
    """
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Load environment variables from .env file
    load_dotenv()

    # Configure Google Generative AI with API key from environment variable
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config, system_instruction=system_prompt)
    response = model.generate_content([question, image_data])
    return response.text

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.json
    question = data.get('question')
    image_path = data.get('image_path')
    
    if not question or not image_path:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Convert image to base64
    image_data_base64 = Image.open(image_path)
    if image_data_base64 is None:
        return jsonify({'error': 'Failed to process the image'}), 400
    
    # Generate response from Gemini model
    response_text = get_gemini_response(question, image_data_base64)
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
