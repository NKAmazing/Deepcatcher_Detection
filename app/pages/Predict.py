import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Model paths
model_paths = ['../detection_model/models/model_0.h5', '../detection_model/models/model_1.h5', '../detection_model/models/model_2.h5', '../detection_model/models/model_3.h5']

# Load the model
model = tf.keras.models.load_model(model_paths[3])

# Function to preprocess the uploaded image
def preprocess_image(image, target_size):
    try:
        img = Image.open(image)
        img = img.convert("RGB")  # Convertir a RGB (en caso de que la imagen tenga canales alpha)
        img = img.resize(target_size)  # Resize
        img = np.array(img) / 255.0    # Normalizar
        img = np.expand_dims(img, axis=0)  # Añadir dimensión del lote
        return img
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Function to perform prediction
def predict(image_data, model):
    try:
        classes = ['Fake', 'Real']
        prediction = model.predict(image_data)
        print(prediction)
        pred_values = tf.squeeze(prediction).numpy()
        print(pred_values)
        prediction = classes[tf.argmax(pred_values)]
        print(prediction)
        confidence = pred_values[tf.argmax(pred_values)]*100
        return prediction, confidence
    except Exception as e:
        st.error(f"Prediction Error: {str(e)}")
        return None, None

# Main Streamlit app
def main():
    st.title('Image Classification: Real vs. Fake')
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        num_images = len(uploaded_files)
        cols = st.columns(num_images)  # Create columns for each image

        for i, uploaded_file in enumerate(uploaded_files):
            # Preprocess the uploaded image
            image = preprocess_image(uploaded_file, target_size=(96, 96))

            if image is not None:
                # Perform prediction
                predicted_class, confidence = predict(image, model)

                if predicted_class is not None:
                    # Display prediction result
                    cols[i].image(uploaded_file, caption=f'Uploaded Image ({predicted_class}, {confidence:.2f}%)', use_column_width=True)

if __name__ == '__main__':
    main()