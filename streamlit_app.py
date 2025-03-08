import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import easyocr
import os
import base64
from io import BytesIO

# Force CPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Set page configuration
st.set_page_config(
    page_title="Camera OCR App",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS and JavaScript for native camera
st.markdown("""
    <style>
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-size: 1.2rem;
            margin-top: 1rem;
            background-color: #FF4B4B;
            color: white;
        }
        #captured-image {
            width: 100%;
            max-width: 800px;
            margin: 1rem auto;
        }
    </style>
""", unsafe_allow_html=True)

# JavaScript for handling native camera
js_code = """
<input type="file" id="camera-input" accept="image/*" capture="environment" style="display: none;">
<button onclick="document.getElementById('camera-input').click();" 
    style="width: 100%; height: 3rem; font-size: 1.2rem; margin: 1rem 0; 
    background-color: #FF4B4B; color: white; border: none; border-radius: 0.3rem; 
    cursor: pointer;">
    📸 Open Camera
</button>
<img id="captured-image" style="display: none;">

<script>
    document.getElementById('camera-input').onchange = function(e) {
        var file = e.target.files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('captured-image').src = e.target.result;
            document.getElementById('captured-image').style.display = 'block';
            // Send to Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: e.target.result
            }, '*');
        };
        reader.readAsDataURL(file);
    };
</script>
"""

@st.cache_resource(show_spinner=False)
def load_ocr():
    try:
        return easyocr.Reader(['en'], gpu=False)
    except Exception as e:
        st.error(f"Error loading OCR model: {str(e)}")
        return None

def draw_boxes(image, bounds, color=(0, 255, 0), width=3):
    try:
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        elif not isinstance(image, Image.Image):
            raise ValueError("Unsupported image type")

        draw_image = image.copy()
        draw = ImageDraw.Draw(draw_image)

        for bound in bounds:
            p0, p1, p2, p3 = bound[0]
            draw.line([tuple(p0), tuple(p1), tuple(p2), tuple(p3), tuple(p0)],
                     fill=color, width=width)

        return draw_image
    except Exception as e:
        st.error(f"Error drawing boxes: {str(e)}")
        return image

def process_image(image):
    try:
        # Convert and process image
        image_np = np.array(image)
        results = st.session_state.ocr_reader.readtext(image_np)
        
        # Show results in a clean layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Original Photo")
            st.image(image, use_container_width=True)
        
        with col2:
            st.markdown("### Detected Text Regions")
            annotated_image = draw_boxes(image, results)
            st.image(annotated_image, use_container_width=True)
        
        # Show extracted text in a clean format
        st.markdown("### 📝 Extracted Text")
        if not results:
            st.warning("No text was detected. Please try again with a clearer photo.")
        else:
            extracted_text = ""
            for result in results:
                text, confidence = result[1], result[2]
                extracted_text += f"{text}\n"
                st.markdown(f"""
                    <div style='
                        background-color: #f0f2f6;
                        padding: 1rem;
                        border-radius: 0.5rem;
                        margin: 0.5rem 0;
                    '>
                        <p style='font-size: 1.2rem; margin: 0;'>{text}</p>
                        <p style='color: #666; margin: 0;'>Confidence: {confidence:.2f}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Download button
            st.download_button(
                "💾 Download Extracted Text",
                extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")

def main():
    st.title("📸 Smart Text Scanner")
    
    # Initialize OCR
    if 'ocr_reader' not in st.session_state:
        with st.spinner("Loading OCR model..."):
            st.session_state.ocr_reader = load_ocr()

    # Create two tabs
    tab1, tab2 = st.tabs([
        "📸 Take Photo",
        "📁 Upload Image"
    ])

    with tab1:
        st.markdown("### Take a Photo of Text")
        
        # Insert the custom camera component
        st.components.v1.html(js_code, height=600)
        
        # Get the captured image from session state
        if 'captured_image' in st.session_state:
            try:
                # Convert base64 to image
                img_data = base64.b64decode(st.session_state.captured_image.split(',')[1])
                image = Image.open(BytesIO(img_data))
                process_image(image)
            except Exception as e:
                st.error(f"Error processing captured image: {str(e)}")

    with tab2:
        st.markdown("### Upload an Image")
        uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                process_image(image)
            except Exception as e:
                st.error(f"Error processing uploaded image: {str(e)}")

    # Helpful tips in expandable section
    with st.expander("📌 Tips for Better Results"):
        st.markdown("""
            ### For Best Results:
            - Ensure good lighting
            - Hold the camera steady
            - Keep text horizontal
            - Avoid glare and shadows
            - Position text within frame
            - Make sure text is in focus
        """)

if __name__ == "__main__":
    main()
