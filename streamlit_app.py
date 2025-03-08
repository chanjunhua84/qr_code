import streamlit as st
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# Initialize PaddleOCR with angle classification and language set to English
ocr = PaddleOCR(use_angle_cls=True, lang="en")

st.title("Better OCR with PaddleOCR")

# Upload an image
uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Open the image using PIL (Python Imaging Library)
    image = Image.open(uploaded_file)
    
    # Display the uploaded image in the Streamlit app
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert the image to a numpy array (required by PaddleOCR)
    img_np = np.array(image)

    # Perform OCR on the image (detects text)
    result = ocr.ocr(img_np, cls=True)
    
    # Display the detected text
    st.subheader("Detected Text:")
    for line in result:
        for word in line:
            # Each 'word' is a list where the second element is the detected text
            st.write(f"Detected Text: {word[1][0]}")
