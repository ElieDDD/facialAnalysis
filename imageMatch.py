import streamlit as st
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np

# Function to calculate SSIM score between two images
def calculate_ssim(image1, image2):
    # Convert images to grayscale
    image1_gray = np.array(image1.convert('L'))
    image2_gray = np.array(image2.convert('L'))
    
    # Compute SSIM between two images
    score, _ = ssim(image1_gray, image2_gray, full=True)
    return score

# Function to compare uploaded image with image1 and image2
def compare_images(uploaded_image, image1, image2):
    # Calculate SSIM for the uploaded image against image1 and image2
    ssim_image1 = calculate_ssim(uploaded_image, image1)
    ssim_image2 = calculate_ssim(uploaded_image, image2)
    
    # Calculate percentage match for each image
    match_image1 = ssim_image1 * 100
    match_image2 = ssim_image2 * 100
    
    # Determine which image the uploaded image is closest to
    if ssim_image1 > ssim_image2:
        return f"Image 1 is the closest match with a similarity of {match_image1:.2f}%", match_image1
    else:
        return f"Image 2 is the closest match with a similarity of {match_image2:.2f}%", match_image2

# Streamlit UI
st.title('Image Similarity Checker')

# Uploading the image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# Open predefined images (image1.jpg, image2.jpg)
try:
    image1 = Image.open("image1.jpg")  # Replace with path to your predefined image1
    image2 = Image.open("image2.jpg")  # Replace with path to your predefined image2
except FileNotFoundError:
    st.error("Predefined images (image1.jpg and image2.jpg) are not found. Please place them in the same directory.")
    image1 = image2 = None

if uploaded_file is not None and image1 and image2:
    # Load uploaded image
    uploaded_image = Image.open(uploaded_file)
    
    # Display uploaded image
    st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)
    
    # Compare the uploaded image with image1 and image2
    result, match_percentage = compare_images(uploaded_image, image1, image2)
    
    # Display the result
    st.write(result)
    st.write(f"SSIM Score for Image 1: {match_percentage:.2f}%")
    st.write(f"SSIM Score for Image 2: {100 - match_percentage:.2f}%")
