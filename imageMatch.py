import streamlit as st
from deepface import DeepFace
from PIL import Image

def main():
    st.title("Facial Image Comparison App")

    # Load the two predefined images
    image1_path = "image1.jpg"
    image2_path = "image2.jpg"

    # Ensure the images are loaded correctly
    try:
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)
    except Exception as e:
        st.error(f"Failed to load one or both of the predefined images: {e}")
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
        # Save the uploaded file temporarily
        uploaded_image_path = "uploaded_image.jpg"
        with open(uploaded_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image
        st.image(uploaded_image_path, caption="Uploaded Image", use_column_width=True)

        # Compare the uploaded image with the two predefined images using DeepFace
        try:
            # Compare with Image 1
            result1 = DeepFace.verify(img1_path=uploaded_image_path, img2_path=image1_path, model_name="VGG-Face")
            # Compare with Image 2
            result2 = DeepFace.verify(img1_path=uploaded_image_path, img2_path=image2_path, model_name="VGG-Face")

            # Display the results
            st.write("Comparison Results:")
            st.write(f"Similarity with Image 1: {result1['distance']:.2f}")
            st.write(f"Similarity with Image 2: {result2['distance']:.2f}")

            # Determine which image is the closest match
            if result1["distance"] < result2["distance"]:
                st.success("The uploaded image is closer to Image 1.")
            else:
                st.success("The uploaded image is closer to Image 2.")

        except Exception as e:
            st.error(f"An error occurred during comparison: {e}")

if __name__ == "__main__":
    main()
