import streamlit as st
from utils.data_loader import validate_uploaded_image, get_image_metadata

def render_upload_widget():
    """
    Renders File Uploader with drag & drop support, metadata preview, and image validation.
    Returns: (uploaded_file, pil_image, metadata, is_valid, error_msg)
    """
    st.markdown("### 📥 Upload Fabric Image")
    st.markdown("<p style='color: #94a3b8; font-size: 0.95rem;'>Supported Formats: <strong>PNG, JPG, JPEG, BMP</strong></p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        label="Drag & Drop or browse fabric image",
        type=["png", "jpg", "jpeg", "bmp"],
        key="fabric_uploader"
    )
    
    if uploaded_file is None:
        return None, None, None, False, None
        
    is_valid, error_msg, pil_img = validate_uploaded_image(uploaded_file)
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
        return uploaded_file, None, None, False, error_msg
        
    metadata = get_image_metadata(uploaded_file, pil_img)
    
    # Display preview and metadata cards
    col_img, col_meta = st.columns([1, 1])
    
    with col_img:
        st.image(pil_img, caption="Uploaded Original Image", use_container_width=True)
        
    with col_meta:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Image Metadata")
        st.markdown(f"**Filename:** `{metadata['filename']}`")
        st.markdown(f"**Resolution:** `{metadata['resolution']}`")
        st.markdown(f"**File Size:** `{metadata['size_str']}`")
        st.markdown(f"**Format:** `{metadata['format']}`")
        st.markdown("</div>", unsafe_allow_html=True)
        
    return uploaded_file, pil_img, metadata, True, None
