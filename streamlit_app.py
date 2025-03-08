import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.last_text = ""
        self.frame_count = 0
        self.process_every_n_frames = 30

    def transform(self, frame):
        self.frame_count += 1
        img = frame.to_ndarray(format="bgr24")
        
        if self.frame_count % self.process_every_n_frames == 0:
            results = self.reader.readtext(img)
            
            for detection in results:
                bbox, text, score = detection
                if score > 0.2:
                    points = np.array(bbox, np.int32)
                    cv2.polylines(img, [points], True, (0, 255, 0), 2)
                    cv2.putText(img, text, tuple(points[0]), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    self.last_text = text
                    
                    # Store detected text in session state
                    if 'detected_texts' not in st.session_state:
                        st.session_state.detected_texts = []
                    if text not in st.session_state.detected_texts:
                        st.session_state.detected_texts.append(text)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("Back Camera OCR Scanner")
    
    # WebRTC configuration
    rtc_configuration = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    
    # Specify back camera
    camera_constraints = {
        "video": {
            "facingMode": {"exact": "environment"}  # This specifies back camera
        },
        "audio": False
    }

    # Create WebRTC streamer
    webrtc_ctx = webrtc_streamer(
        key="camera",
        video_transformer_factory=VideoTransformer,
        rtc_configuration=rtc_configuration,
        media_stream_constraints=camera_constraints,
        async_processing=True
    )
    
    # Display detected texts
    if 'detected_texts' in st.session_state and st.session_state.detected_texts:
        st.subheader("Detected Text:")
        for text in st.session_state.detected_texts:
            st.write(text)
        
        # Add clear button
        if st.button("Clear Detected Text"):
            st.session_state.detected_texts = []
            st.experimental_rerun()
        
        # Add download button
        if st.download_button(
            label="Download Text",
            data="\n".join(st.session_state.detected_texts),
            file_name="scanned_text.txt",
            mime="text/plain"
        ):
            st.success("Text downloaded successfully!")

    # Mobile-friendly styling
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stVideo {
            width: 100%;
            height: auto;
        }
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
    1. Allow camera access when prompted
    2. Use your back camera to scan text
    3. Hold steady for better results
    4. Detected text will appear below
    5. Download or clear text as needed
    """)

    # Settings in sidebar
    with st.sidebar:
        st.header("Scanner Settings")
        confidence = st.slider("Confidence Threshold", 0.0, 1.0, 0.2)
        scan_frequency = st.slider("Scan Frequency", 1, 60, 30, 
                                 help="Process every N frames")

if __name__ == "__main__":
    main()
