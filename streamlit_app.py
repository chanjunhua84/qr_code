import easyocr
from PIL import Image
import streamlit as st

st.title("EasyOCR Example")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # OCR using EasyOCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    
    st.subheader("Detected Text:")
    for detection in result:
        st.write(detection[1])  # detection[1] contains the recognized text
