import streamlit as st
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
import io

def calculate_ssim(image1, image2):
    # Convert images to grayscale
    image1_gray = np.array(image1.convert('L'))
    image2_gray = np.array(image2.convert('L'))
    
    # Compute SSIM between two images
    score, _ = ssim(image1_gray, image2_gray, full=True)
    return score

def compare_images(uploaded_image, image1, image2):
    # Calculate SSIM for the uploaded image against image1 and image2
    ssim_image1 = calculate_ssim(uploaded_image, image1)
    ssim_image2 = calculate_ssim(uploaded_image, image2)
    
    # Determine which image the uploaded image is closest to
    if ssim_image1 > ssim_image2:
        return "Image 1 is the closest match!"
    else:
        return "Image 2 is the closest match!"

# Streamlit UI
st.title('Image Similarity Checker')

# Uploading the images
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# Open predefined images (image1, image2)
image1 = Image.open("image1.jpg")  # Predefined image 1 path
image2 = Image.open("image2.jpg")  # Predefined image 2 path

if uploaded_file is not None:
    # Load uploaded image
    uploaded_image = Image.open(uploaded_file)
    
    # Display uploaded image
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
    
    # Compare with predefined images
    result = compare_images(uploaded_image, image1, image2)
    st.write(result)
