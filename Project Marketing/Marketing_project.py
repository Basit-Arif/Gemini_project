import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
import os 
from PIL import Image
import io
import tempfile
import pathlib
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
st.title("🚀 Product Description Generator 🌟")

# Display subtitle with emoji
st.markdown("### Generate Marketing-Oriented Product Descriptions 📸")
st.sidebar.header("Brand Brilliance: Enhance Your Brand with Engaging Descriptions")

def save_uploaded_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())

    return temp_file.name
genai.configure(api_key=st.secrets["GoogleApikey"]["api_key"])
st.sidebar.markdown("---")
pictures=st.sidebar.file_uploader("Upload Image",type=["Jpeg","Jpg","webp","png"],accept_multiple_files=True)
from typing import Union
class post(BaseModel):
    Post:str
    Product_name:str
    Product_description:str

parser=PydanticOutputParser(pydantic_object=post)
def get_responce(picture):
    model=genai.GenerativeModel("gemini-pro-vision")
    responce=model.generate_content(
        glm.Content(
            parts=[
            glm.Part(text=f"Create unique and compelling marketing-oriented descriptions for products, analyzing each provided image to highlight their distinct features, benefits, and the brand name (which is {brandname}). The descriptions should emphasize the product's uniqueness and include a call-to-action message at the end. Ensure each description captures the product's essence, resonates with the target audience, and encourages engagement  .\
                  {parser.get_format_instructions()} \
                  \
                    `Post`: Craft an engaging and distinctive marketing-oriented description that vividly highlights the product's key features, benefits, and resonates with the intended audience. Ensure the description encapsulates the product's uniqueness, addresses its advantages, and concludes with an impactful call-to-action, encouraging audience engagement,\
                    `Product_name``: [Identified product name from the image],\
                    `Product_description``: [Create compelling narratives that emphasize the standout attributes and benefits and make it short intro of product]\
\
             "),
            glm.Part(
                inline_data=glm.Blob(
                    mime_type='image/jpeg',
                    data=pathlib.Path(picture).read_bytes()
                )
            ),  
        ]),
stream=True)
    responce.resolve()
    return responce
st.sidebar.markdown("---")
col1, col2 = st.columns([2, 2])
brandname=st.sidebar.text_input("Enter Your Brand Name")

if st.sidebar.button('Click button to generate text') and brandname != "":
    if pictures:
        for i, picture in enumerate(pictures):
            image_url = save_uploaded_file(picture)
            try:
                if i % 2 == 0:
                    with col1:
                        st.image(image_url) 
                        response = get_responce(image_url)
                        parsed_output = parser.parse(response.text)
                        st.markdown("<br>**Social Media Post**</br>", unsafe_allow_html=True)
                        st.write(parsed_output.Post)
                        # st.markdown("<br style='color:blue;'>**Product Name**</br>", unsafe_allow_html=True)
                        st.write(parsed_output.Product_name)
                        st.markdown("<br>**Product Description**</br>", unsafe_allow_html=True)
                        st.write(parsed_output.Product_description)
                        

                else:
                    with col2:
                        st.image(image_url)
                        response = get_responce(image_url)
                        parsed_output = parser.parse(response.text)
                        st.markdown("<br>**Social Media Post**</br>", unsafe_allow_html=True)
                        st.write(parsed_output.Post)
                        st.markdown("<br>**Product Name**</br>", unsafe_allow_html=True)
                        st.write(parsed_output.Product_name)
                        st.markdown("<br>**Product Description**</br>", unsafe_allow_html=True)
                        st.write(parsed_output.Product_description)
            except :
                pass
