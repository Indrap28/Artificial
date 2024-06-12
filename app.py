import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.set_page_config(page_title='Welcome')
st.header('Elite Species App')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button('Tell me the about Specimen')

input_prompt="""
You are an Zoological expert where you need to see the pets from the image
               and identify the breed, also provide the details of breed nature 
               is below format

               1. Kingdom -  level of biological classification : 
               2. Category - type of animla like cat, dog etc
               3. Breed - type of breed
               4. Lifespan - No of Years they live
               5. Weight - Maximum Weight
               6. Color - Color to identify its purity
               7. Domestic - Whether can be kept as pet or not
               8. favorit food - Food they eat most
               9. Get furious with - What makes them Angry,furious and aggressive
               
     Give Short desciption about its nature in 40 words
               ----
               ----
    Finally also mention approximate monthly expense behind the pet in Indian Rupees if its domestic or else if Not domestic 
    mention its monthly expense in Indian Rupees if kept in Zoo.

"""


if submit:
    image_data=input_image_setup(uploaded_file)
    response= get_gemini_response(input_prompt, image_data)
    st.header('The details about the Specimen are as follow:')
    st.write(response)



