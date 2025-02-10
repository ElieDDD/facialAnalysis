import streamlit as st
from PIL import Image
import numpy as np

def calculate_mse(image1, image2):
    # Calculate the Mean Squared Error between two images
    err = np.sum((np.array(image1).astype("float") - np.array(image2).astype("float")) ** 2)
    err /= float(image1.size[0] * image1.size[1])
    return err

def main():
    st.title("Image Comparison App")
    
    # Load the two predefined images
    image1 = Image.open("image1.jpg")
    image2 = Image.open("image2.jpg")
    
    # Ensure the images are loaded correctly
    if image1 is None or image2 is None:
        st.error("Failed to load one or both of the predefined images.")
        return
    
    # Display the predefined images
    st.write("Predefined Images:")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption="Image 1", use_column_width=True)
    with col2:
        st.image(image2, caption="Image 2", use_column_width=True)
    
    # Upload a new image
    uploaded_file = st.file_uploader("Upload an image to compare:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Convert the uploaded file to a PIL image
        uploaded_image = Image.open(uploaded_file)
        
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        # Resize images to the same dimensions for comparison
        target_size = (min(image1.size[0], image2.size[0], uploaded_image.size[0]),
                       min(image1.size[1], image2.size[1], uploaded_image.size[1]))
        
        image1_resized = image1.resize(target_size)
        image2_resized = image2.resize(target_size)
        uploaded_image_resized = uploaded_image.resize(target_size)
        
        # Calculate MSE between the uploaded image and the two predefined images
        mse1 = calculate_mse(uploaded_image_resized, image1_resized)
        mse2 = calculate_mse(uploaded_image_resized, image2_resized)
        
        # Determine which image is the closest match
        if mse1 < mse2:
            st.success("The uploaded image is closer to Image 1.")
        else:
            st.success("The uploaded image is closer to Image 2.")
        
        # Display the MSE values
        st.write(f"MSE between Uploaded Image and Image 1: {mse1:.2f}")
        st.write(f"MSE between Uploaded Image and Image 2: {mse2:.2f}")

if __name__ == "__main__":
    main()
