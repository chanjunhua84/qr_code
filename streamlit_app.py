# Alternative simpler version
def main():
    st.set_page_config(page_title="Text Scanner", layout="wide")
    
    inject_custom_css()
    
    reader = get_ocr_reader()

    st.markdown('<h1 style="text-align: center; font-size: 36px;">Text Scanner</h1>', 
                unsafe_allow_html=True)

    # Camera input with back camera configuration
    img_file = st.camera_input(
        "",
        key="camera",
        help="",
        on_change=None,
        disabled=False,
        label_visibility="hidden"
    )

    if img_file:
        image = Image.open(img_file)
        
        with st.spinner('Reading text...'):
            results = perform_ocr(image, reader)
            
            all_text = []
            for result in results:
                text = result[1]
                confidence = result[2]
                if confidence > 0.2:
                    all_text.append(text)
                    st.markdown(f'<div class="large-text">{text}</div>', 
                              unsafe_allow_html=True)
            
            if all_text:
                combined_text = "\n".join(all_text)
                st.download_button(
                    "💾 SAVE TEXT",
                    data=combined_text,
                    file_name="scanned_text.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        if st.button("📸 SCAN ANOTHER", use_container_width=True):
            st.rerun()
    else:
        st.markdown("""
            <div class="large-text" style="margin-top: 40px;">
            Tap the camera button above to take a photo
            </div>
        """, unsafe_allow_html=True)
