import streamlit as st
import cv2
import numpy as np

def calculate_mse(image1, image2):
    # Calculate the Mean Squared Error between two images
    err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
    err /= float(image1.shape[0] * image1.shape[1])
    return err

def main():
    st.title("Image Comparison App")
    
    # Load the two predefined images
    image1 = cv2.imread("image1.jpg")
    image2 = cv2.imread("image2.jpg")
    
    # Ensure the images are loaded correctly
    if image1 is None or image2 is None:
        st.error("Failed to load one or both of the predefined images.")
        return
    
    # Convert images to RGB (OpenCV loads images in BGR)
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
    
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
        # Convert the uploaded file to an OpenCV image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        uploaded_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        uploaded_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2RGB)
        
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        
        # Resize images to the same dimensions for comparison
        target_size = (min(image1.shape[1], image2.shape[1], uploaded_image.shape[1]),
                       min(image1.shape[0], image2.shape[0], uploaded_image.shape[0]))
        
        image1_resized = cv2.resize(image1, target_size)
        image2_resized = cv2.resize(image2, target_size)
        uploaded_image_resized = cv2.resize(uploaded_image, target_size)
        
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
