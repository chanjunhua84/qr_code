import streamlit as st
import qrcode
import numpy as np
import cv2
from PIL import Image

st.title("QR Code Generator & Scanner")

# Tabs for Generate & Scan
tab1, tab2 = st.tabs(["Generate QR Code", "Scan QR Code"])

# 🔹 QR Code Generator
with tab1:
    st.subheader("Generate QR Code")
    text = st.text_input("Enter text to generate QR code:")
    
    if st.button("Generate QR Code"):
        if text:
            qr = qrcode.QRCode(
                version=1, box_size=10, border=5
            )
            qr.add_data(text)
            qr.make(fit=True)
            qr_img = qr.make_image(fill="black", back_color="white")

            st.image(qr_img, caption="Generated QR Code", use_column_width=True)
            st.success("QR Code generated successfully!")
        else:
            st.warning("Please enter text to generate a QR code.")

# 🔹 QR Code Scanner
with tab2:
    st.subheader("Scan QR Code")
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded QR Code", use_column_width=True)

        # Convert image for OpenCV
        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Detect and Decode QR Code
        detector = cv2.QRCodeDetector()
        qr_text, _, _ = detector.detectAndDecode(gray)

        if qr_text:
            st.success(f"Decoded QR Code Text: {qr_text}")
        else:
            st.error("No QR Code detected. Please try another image.")
