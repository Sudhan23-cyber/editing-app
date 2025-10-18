import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="Image Filter App")

st.title("FOXY EDITS App")

# File upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Filter selection — only the filters you want to keep
filter_type = st.selectbox(
    "Select Filter",
    [
        "Original",
        "Grayscale",
        "Brightness +",
        "Brightness -",
        "Contrast +",
        "Contrast -",
    ]
)

if uploaded_file is not None:
    # Read image bytes and decode
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        st.error("Error: could not decode image. Please upload a valid image file.")
    else:
        # Apply filter
        if filter_type == "Original":
            processed = img.copy()
        elif filter_type == "Grayscale":
            processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif filter_type == "Brightness +":
            processed = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
        elif filter_type == "Brightness -":
            processed = cv2.convertScaleAbs(img, alpha=0.8, beta=-30)
        elif filter_type == "Contrast +":
            processed = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
        elif filter_type == "Contrast -":
            processed = cv2.convertScaleAbs(img, alpha=0.7, beta=0)
        else:
            processed = img.copy()

        # Convert to PIL Image for display
        if len(processed.shape) == 2:
            # grayscale
            processed_display = Image.fromarray(processed)
        else:
            # BGR → RGB
            processed_display = Image.fromarray(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))

        # Show images
        st.subheader("Original Image")
        # convert original to RGB for correct display
        orig_display = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        st.image(orig_display, use_column_width=True)

        st.subheader("Processed Image")
        st.image(processed_display, use_column_width=True)
