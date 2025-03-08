import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

def load_model():
    return easyocr.Reader(['en'])

def perform_ocr(image, reader):
    results = reader.readtext(np.array(image))
    return results

def main():
    st.title("Photo OCR Scanner")
    
    # Initialize EasyOCR
    @st.cache_resource
    def get_ocr_reader():
        return load_model()
    
    reader = get_ocr_reader()

    # Camera input using Streamlit's camera_input
    img_file = st.camera_input("Take a picture", help="Uses back camera by default")
    
    if img_file is not None:
        # Convert image to PIL Image
        image = Image.open(img_file)
        
        # Add a process button
        if st.button('Extract Text'):
            with st.spinner('Processing...'):
                # Perform OCR
                results = perform_ocr(image, reader)
                
                # Display results
                st.subheader("Extracted Text:")
                
                # Store all detected text
                all_text = []
                
                for result in results:
                    text = result[1]
                    confidence = result[2]
                    all_text.append(text)
                    st.write(f"Text: {text} (Confidence: {confidence:.2f})")
                
                # Combine all text
                combined_text = "\n".join(all_text)
                
                # Download button
                if all_text:
                    st.download_button(
                        label="Download extracted text",
                        data=combined_text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )

    # Mobile-friendly styling
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stButton button {
            width: 100%;
            margin: 10px 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Instructions
    st.markdown("""
    ### Instructions:
    1. Click 'Take a picture' to open your camera
    2. Take a clear photo of the text
    3. Click 'Extract Text' to process
    4. Download the extracted text if needed
    """)

    # Optional settings in sidebar
    with st.sidebar:
        st.header("Settings")
        confidence_threshold = st.slider(
            "Confidence Threshold", 
            0.0, 1.0, 0.2,
            help="Adjust confidence threshold for text detection"
        )

if __name__ == "__main__":
    main()
