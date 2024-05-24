import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import requests

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
    
def get_user_id(token):
    url_api = "http://127.0.0.1:8000/user/id/"
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url_api, headers=headers)
    if response.status_code == 200:
        return response.json().get('user_id')
    else:
        st.error("Error al obtener el ID del usuario")
        return None

def save_prediction(user_id, predicted_class, confidence, token):
    # Save the prediction using the Django API
    url_api = "http://127.0.0.1:8000/predictions/"
    headers = {'Authorization': f'Token {token}'}
    data = {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'user': user_id,
    }
    response = requests.post(url_api, headers=headers, json=data)
    if response.status_code == 201:
        st.success("Resultado de predicción guardado correctamente en la API.")
    else:
        st.error(f"Error al guardar resultado de predicción: {response.status_code}")

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

                    # Check if the user is authenticated
                    if 'authenticated' in st.session_state and st.session_state.authenticated:
                        # Get user ID and token
                        user_id = get_user_id()

                        print("User ID:", user_id)

                        print("Token:", st.session_state.token)

                        # Save the prediction
                        save_prediction(user_id, predicted_class, confidence, st.session_state.token)

if __name__ == '__main__':
    main()