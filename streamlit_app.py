import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import cv2

# Set page configuration
st.set_page_config(
    page_title="OCR Application",
    page_icon="🔤",
    layout="wide"
)

# Cache the EasyOCR reader
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])  # Initialize for English

def draw_boxes(image, bounds, color='yellow', width=2):
    """Draw bounding boxes on the image"""
    img = np.array(image)
    for bound in bounds:
        p0, p1, p2, p3 = bound[0]
        cv2.line(img, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), color, width)
        cv2.line(img, (int(p1[0]), int(p1[1])), (int(p2[0]), int(p2[1])), color, width)
        cv2.line(img, (int(p2[0]), int(p2[1])), (int(p3[0]), int(p3[1])), color, width)
        cv2.line(img, (int(p3[0]), int(p3[1])), (int(p0[0]), int(p0[1])), color, width)
    return img

def main():
    st.title("🔤 OCR Text Extraction Tool")
    st.write("Upload an image to extract text from it.")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # Display original image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)

        if st.button("Extract Text"):
            with st.spinner("Processing image..."):
                try:
                    # Load OCR reader
                    reader = load_ocr()
                    
                    # Convert image to numpy array
                    image_np = np.array(image)
                    
                    # Perform OCR
                    results = reader.readtext(image_np)
                    
                    # Draw boxes on image
                    annotated_image = draw_boxes(image, results)
                    
                    with col2:
                        st.subheader("Detected Text Regions")
                        st.image(annotated_image, use_column_width=True)

                    # Display results
                    st.subheader("Extracted Text")
                    
                    extracted_text = ""
                    for result in results:
                        text = result[1]
                        confidence = result[2]
                        extracted_text += f"{text}\n"
                        st.write(f"📝 **Text:** {text}")
                        st.write(f"🎯 **Confidence:** {confidence:.2f}")
                        st.write("---")

                    # Download button
                    st.download_button(
                        label="Download extracted text",
                        data=extracted_text,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

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
