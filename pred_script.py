import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Model paths
model_paths = ['detection_model/model.h5', 'detection_model/models/model_1.h5', 'detection_model/models/model_2.h5', 'detection_model/models/model.h5']

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
def predict(image_data, model, threshold=0.5):
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
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Preprocess the uploaded image
        image = preprocess_image(uploaded_file, target_size=(150, 150))

        if image is not None:
            # Perform prediction
            predicted_class, confidence = predict(image, model)

            if predicted_class is not None:
                # Display prediction result
                st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
                st.write(f'This image has a probability of being {predicted_class} with a confidence of {confidence:.2f}%')

if __name__ == '__main__':
    main()