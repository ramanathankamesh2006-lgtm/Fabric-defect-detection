import os
import io
from PIL import Image
import numpy as np

SUPPORTED_FORMATS = ["PNG", "JPG", "JPEG", "BMP"]

def validate_uploaded_image(uploaded_file):
    """
    Validates uploaded image file format and integrity.
    Returns: (is_valid: bool, error_message: str, PIL Image object or None)
    """
    if uploaded_file is None:
        return False, "No file uploaded.", None

    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].replace(".", "").upper()

    if ext not in SUPPORTED_FORMATS:
        return False, f"Unsupported format '.{ext}'. Please upload a PNG, JPG, JPEG, or BMP image.", None

    try:
        image_bytes = uploaded_file.read()
        uploaded_file.seek(0) # Reset stream position
        pil_img = Image.open(io.BytesIO(image_bytes))
        pil_img.verify() # Verify image integrity
        
        # Re-open after verify() call
        uploaded_file.seek(0)
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return True, "Valid image", pil_img
    except Exception as e:
        return False, f"Corrupted or unreadable image file: {str(e)}", None

def get_image_metadata(uploaded_file, pil_img):
    """
    Extracts image resolution, file size, format, and filename details.
    """
    filename = uploaded_file.name
    uploaded_file.seek(0, os.SEEK_END)
    size_bytes = uploaded_file.tell()
    uploaded_file.seek(0)
    
    width, height = pil_img.size
    
    if size_bytes < 1024:
        size_str = f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        size_str = f"{size_bytes / 1024:.1f} KB"
    else:
        size_str = f"{size_bytes / (1024 * 1024):.2f} MB"
        
    return {
        "filename": filename,
        "width": width,
        "height": height,
        "resolution": f"{width} x {height}",
        "size_bytes": size_bytes,
        "size_str": size_str,
        "format": pil_img.format if pil_img.format else os.path.splitext(filename)[1].replace(".", "").upper()
    }
