import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2
import os
import torch

# Force CPU usage to avoid CUDA/MPS issues
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Set page configuration
st.set_page_config(
    page_title="OCR Application",
    page_icon="🔤",
    layout="wide"
)

# Cache the EasyOCR reader
@st.cache_resource(show_spinner=False)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False)  # Force CPU usage
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def draw_boxes(image, bounds, color=(0, 255, 0), width=2):
    """Draw bounding boxes on the image"""
    try:
        img = np.array(image)
        for bound in bounds:
            p0, p1, p2, p3 = bound[0]
            points = np.array([[int(p0[0]), int(p0[1])],
                             [int(p1[0]), int(p1[1])],
                             [int(p2[0]), int(p2[1])],
                             [int(p3[0]), int(p3[1])]], np.int32)
            cv2.polylines(img, [points], True, color, width)
        return img
    except Exception as e:
        st.error(f"Error drawing boxes: {str(e)}")
        return np.array(image)

def main():
    st.title("🔤 OCR Text Extraction Tool")
    st.write("Upload an image to extract text from it.")

    # Initialize session state if not exists
    if 'ocr_reader' not in st.session_state:
        with st.spinner("Loading OCR model..."):
            st.session_state.ocr_reader = load_ocr()

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        try:
            # Display original image
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Original Image")
                image = Image.open(uploaded_file)
                st.image(image, use_container_width=True)  # Updated parameter

            if st.button("Extract Text"):
                if st.session_state.ocr_reader is None:
                    st.error("OCR model failed to load. Please refresh the page.")
                    return

                with st.spinner("Processing image..."):
                    try:
                        # Convert image to numpy array
                        image_np = np.array(image)
                        
                        # Perform OCR
                        results = st.session_state.ocr_reader.readtext(image_np)
                        
                        # Draw boxes on image
                        annotated_image = draw_boxes(image, results)
                        
                        with col2:
                            st.subheader("Detected Text Regions")
                            st.image(annotated_image, use_container_width=True)  # Updated parameter

                        # Display results
                        st.subheader("Extracted Text")
                        
                        if not results:
                            st.warning("No text was detected in the image.")
                        else:
                            extracted_text = ""
                            for result in results:
                                text = result[1]
                                confidence = result[2]
                                extracted_text += f"{text}\n"
                                st.write(f"📝 **Text:** {text}")
                                st.write(f"🎯 **Confidence:** {confidence:.2f}")
                                st.write("---")

                            # Download button
                            if extracted_text.strip():
                                st.download_button(
                                    label="Download extracted text",
                                    data=extracted_text,
                                    file_name="extracted_text.txt",
                                    mime="text/plain"
                                )

                    except Exception as e:
                        st.error(f"Error processing image: {str(e)}")

        except Exception as e:
            st.error(f"Error loading image: {str(e)}")

    # Add information sidebar
    st.sidebar.title("ℹ️ Information")
    st.sidebar.write("""
    ### Supported Formats
    - PNG
    - JPEG
    - JPG
    
    ### Tips for better results
    - Use clear, high-resolution images
    - Ensure good contrast between text and background
    - Avoid skewed or rotated text
    """)

if __name__ == "__main__":
    main()
