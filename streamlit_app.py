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
        self.process_every_n_frames = 30  # Process every 30 frames to reduce load

    def transform(self, frame):
        self.frame_count += 1
        img = frame.to_ndarray(format="bgr24")
        
        # Process every nth frame
        if self.frame_count % self.process_every_n_frames == 0:
            # Perform OCR
            results = self.reader.readtext(img)
            
            # Draw boxes and text on image
            for detection in results:
                bbox, text, score = detection
                if score > 0.2:  # Confidence threshold
                    points = np.array(bbox, np.int32)
                    cv2.polylines(img, [points], True, (0, 255, 0), 2)
                    cv2.putText(img, text, tuple(points[0]), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    self.last_text = text
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("Real-time Camera OCR")
    
    # WebRTC configuration
    rtc_configuration = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    
    # Create a placeholder for the text output
    text_placeholder = st.empty()
    
    # Create WebRTC streamer
    webrtc_ctx = webrtc_streamer(
        key="camera",
        video_transformer_factory=VideoTransformer,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"video": True, "audio": False}
    )
    
    # Instructions
    st.markdown("""
    ### Instructions:
    1. Allow camera access when prompted
    2. Point your camera at text you want to scan
    3. Hold the camera steady for best results
    4. Detected text will appear below the video
    """)
    
    # Add mobile-friendly CSS
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stVideo {
            width: 100%;
            height: auto;
        }
    }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
