from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up Streamlit app
st.title("Gemini-Testing")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image (but don't display it)
    image = Image.open(uploaded_file)

    # Save the uploaded file temporarily
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Create the model
    generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    system_prompt = """You are an excellent Invoice analyzer. 
    Your job is to read the invoice image provided to you correctly in the first try. 
    You have to be accruate with your readings. 
    You have to only give the output of the read data in a json format and nothing else. Make sure you include the units of the items etc.
    Also add spacing of newlines so the json response looks nice.
    If the data in invoice is in a different language other than english then translate it to english and put the translated response in the json data.
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction= system_prompt
    )

    # System prompt and query (fixed)
    query_prompt = "Read the invoice and give me all the details you read on it"

    if st.button('Run Query'):
        try:
            # Send the query
            response = model.generate_content([query_prompt,image])

            # Display the result
            st.subheader("Result:")
            st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Clean up the temporary file
    os.remove("temp_image.jpg")