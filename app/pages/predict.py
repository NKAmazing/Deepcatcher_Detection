import streamlit as st
from streamlit_option_menu import option_menu
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
from streamlit_elements import elements, mui

# Model paths
model_paths = ['../detection_model/models/model_0.h5', '../detection_model/models/model_1.h5', 
               '../detection_model/models/model_2.h5', '../detection_model/models/model_3.h5',
               '../detection_model/models/model_4.h5']

# Load the model
model = tf.keras.models.load_model(model_paths[3])

st.set_page_config(page_title="Deepcatcher Demo", page_icon=":globe_with_meridians:")

# layout="wide", initial_sidebar_state="expanded"

st.sidebar.title("Deepcatcher Demo")

options = st.sidebar.radio("Select an option: ", ["Main Menu"])

# Function to preprocess the uploaded image
def preprocess_image(image, target_size):
    '''
    Function to preprocess the uploaded image for prediction
    params:
        image: Uploaded image
        target_size: Target size for the image
    '''
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
    '''
    Function to perform prediction on the image data using the model
    params:
        image_data: Preprocessed image data
        model: Trained model
    '''
    try:
        classes = ['Fake', 'Real']
        prediction = model.predict(image_data)
        pred_values = tf.squeeze(prediction).numpy()
        prediction = classes[tf.argmax(pred_values)]
        confidence = pred_values[tf.argmax(pred_values)] * 100
        return prediction, confidence
    except Exception as e:
        st.error(f"Prediction Error: {str(e)}")
        return None, None

def get_user_id(token):
    '''
    Function to get the user ID from the API using the token
    params:
        token: Token of the authenticated user
    '''
    url_api = "http://127.0.0.1:8000/user-service/user/id/"
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url_api, headers=headers)
    if response.status_code == 200:
        return response.json().get('user_id')
    else:
        st.error("Error at getting the User ID.")
        return None

def save_prediction(user_id, predicted_class, confidence, image_file, token):
    '''
    Function to save the prediction result in the API
    params:
        user_id: User ID
        predicted_class: Predicted class of the image (Real/Fake)
        confidence: Confidence of the prediction
        image_file: Uploaded image file to save
        token: Token of the authenticated user
    '''
    url_api = "http://127.0.0.1:8000/user-service/predictions/"
    headers = {'Authorization': f'Token {token}'}
    files = {'image': image_file}
    data = {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'user': user_id,
    }
    response = requests.post(url_api, headers=headers, data=data, files=files)
    if response.status_code == 201:
        success_message = "Prediction successfully saved in the API."
        st.success(success_message)
    else:
        error_message = f"Error at saving the prediction result: {response.status_code} - {response.json()}"
        st.error(error_message)

# ----------------------------------------------------------------------------------------------------------------
# Delete Functionality
# ----------------------------------------------------------------------------------------------------------------

def delete_prediction(prediction_id, token):
    ''' 
    Function to delete request to the API to delete a prediction
    params:
        prediction_id: Prediction ID to delete
        token: Token of the authenticated user
    '''
    url_api = f"http://127.0.0.1:8000/user-service/predictions/{prediction_id}/"
    headers = {'Authorization': f'Token {token}'}
    print("URL: ", url_api)  # Debugging print statement
    response = requests.delete(url_api, headers=headers)
    if response.status_code == 204:
        return True, None  # Success, no error message
    else:
        return False, f"Error deleting the prediction: {response.status_code} - {response.json()}"

# Function to create a delete callback
def create_delete_callback(prediction_id, token, success_callback, error_callback):
    ''' 
    Define the callback function to set the prediction ID and 
    token and calls the delete_prediction function
    params:
        prediction_id: Prediction ID to delete
        token: Token of the authenticated user
        success_callback: Callback function to handle success message
        error_callback: Callback function to handle error message
    '''
    def callback():
        success, error_message = delete_prediction(prediction_id, token)
        if success:
            success_callback()
        else:
            error_callback(error_message)
    return callback

# ----------------------------------------------------------------------------------------------------------------
# Prediction History View
# ----------------------------------------------------------------------------------------------------------------

def get_prediction_history(user_id, token):
    '''
    Function to get request to the API to get the prediction history for a user
    params:
        user_id: User ID
        token: Token of the authenticated user
    '''
    url_api = f"http://127.0.0.1:8000/user-service/predictions/?user={user_id}"
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url_api, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error at getting predictions history for this user.")
        st.error(f"The Error was: {response.status_code} - {response.json()}")
        return []

def display_prediction_history(predictions, token):
    '''
    Display the prediction history in a card format 
    using Mui components of Streamlit-Elements
    params:
        predictions: List of prediction history
        token: Token of the authenticated user
    '''
    if predictions:
        st.subheader('Predictions History')

        # Set the elements container to display the history
        with elements("history"):

            # Sort by timestamp descending
            predictions = sorted(predictions, key=lambda x: x['timestamp'], reverse=True)  

            # Iterate over the predictions
            for prediction in predictions:

                # Ensure the ID is captured correctly
                prediction_id = prediction['id']  

                # Determine the color of the typography based on the predicted class
                color = "green" if prediction['predicted_class'] == 'Real' else "red"

                # Placeholder to display the prediction
                placeholder = st.empty()

                # Display the prediction in a card format
                with mui.Card(sx={"maxWidth": 700, "margin": "20px auto", "border-radius": 10, 
                                  "border": f"2px solid {color}", 
                                  "boxShadow": "0 0 10px rgba(0, 0, 0, 0.1)"}, 
                                  variant="outlined"):
                    # Card content
                    with mui.Grid(container=True, spacing=2):
                        # Display the image of the prediction
                        with mui.Grid(item=True, xs=12, sm=3):
                            mui.CardMedia(
                                component="img",
                                height="auto",
                                width="100%",
                                image=prediction['image'],  
                                alt="Image Prediction"
                            )
                        # Display the prediction details
                        with mui.Grid(item=True, xs=12, sm=8):
                            mui.CardContent(sx={"height": "100%"})(
                                # Showing Predicted Class
                                mui.Typography(
                                    f"{prediction['predicted_class']}",
                                    style={"fontSize": "1.5rem", "fontWeight": "bold", "color": color},
                                    variant="h5"
                                ),
                                mui.Divider(),
                                # Spacer
                                mui.Box(sx={"height": 10}),
                                mui.Typography(
                                    f"Confidence of {prediction['confidence']:.2f}%",
                                    style={"fontSize": "1rem", "fontWeight": "bold"}
                                ),
                                mui.Typography(
                                    # Separate the date and time
                                    f"Saved the date {prediction['timestamp'].split('T')[0]} at {prediction['timestamp'].split('T')[1].split('.')[0]}",
                                    style={"fontSize": "0.9rem"}
                                )
                            )
                    # Card actions
                    with mui.CardActions(sx={"display": "flex", "justifyContent": "space-between"}):
                        # Delete button for the prediction
                        mui.Button(
                            "Delete", 
                            size="small",
                            sx={"backgroundColor": "red", "color": "white", "marginLeft": "auto"},
                            onClick=create_delete_callback(prediction_id, token, 
                                               lambda: show_delete_success(placeholder), 
                                               lambda error_message: show_delete_error(placeholder, error_message))  # Use the callback function
                        )
    else:
        st.info('No hay predicciones disponibles.')

def show_delete_success(placeholder):
    '''
    Show success message after deleting a prediction
    '''
    with placeholder:
        with st.expander("Delete Status", expanded=True):
            st.success(f"Prediction successfully deleted.")

def show_delete_error(placeholder, error_message):
    '''
    Show error message after failed to delete a prediction
    '''
    with placeholder:
        with st.expander("Delete Status", expanded=True):
            st.error(f"Error deleting prediction: {error_message}")

def history_view():
    ''' 
    Prediction history view to display the prediction history 
    '''
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        # Get the user ID
        user_id = get_user_id(st.session_state.token)

        # Display prediction history
        predictions = get_prediction_history(user_id, st.session_state.token)
        display_prediction_history(predictions, st.session_state.token)
    else:
        st.warning('History is empty.')
        st.warning('Please login to view prediction history.')

# ----------------------------------------------------------------------------------------------------------------
# Prediction View
# ----------------------------------------------------------------------------------------------------------------

def predict_view():
    '''
    Prediction view to upload images and display the prediction result
    '''
    # Header title for the predict view
    st.header("Image Classification: Real vs. Fake")
    
    # Set the File Uploader
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        # Set the number of columns per row
        cols_per_row = 3

        if len(uploaded_files) <= 2:
            cols = st.columns(len(uploaded_files))
            for i, uploaded_file in enumerate(uploaded_files):

                # Set the index
                index = i

                # Preprocess the uploaded image
                image = preprocess_image(uploaded_file, target_size=(96, 96))

                if image is not None:
                    # Perform prediction
                    predicted_class, confidence = predict(image, model)

                    if predicted_class is not None:
                        # Display prediction result
                        cols[i].image(uploaded_file, caption=f'Uploaded Image ({predicted_class}, {confidence:.2f}%)', use_column_width=True)

                        # Place the save button in the correct column
                        with cols[i]:
                            # Save prediction button with index image
                            if st.button(f"Save Prediction {index+1}"):
                                # Check if the user is authenticated
                                if 'authenticated' in st.session_state and st.session_state.authenticated:
                                    # Get the user ID
                                    user_id = get_user_id(st.session_state.token)
                                    # Get the current predictions saved of the user
                                    predictions = get_prediction_history(user_id, st.session_state.token)
                                    # Check if the user has already exceeded the limit of 10 saved predictions
                                    if len(predictions) >= 10:
                                        st.warning('You have reached the limit of 10 saved predictions.')
                                    else:
                                        # Save the prediction
                                        with st.expander("Prediction Status", expanded=True):
                                            save_prediction(user_id, predicted_class, confidence, uploaded_file, st.session_state.token)
                                else:
                                    st.warning('Please login to save the prediction.')
        else:
            # Calculate the number of rows based on the number of uploaded files
            rows = (len(uploaded_files) + cols_per_row - 1) // cols_per_row
            # Iterate over the rows and columns to display the uploaded images
            for row in range(rows):
                # Create columns for each row
                cols = st.columns(cols_per_row)

                # Iterate over the columns in each row
                for col_index in range(cols_per_row):

                    # Calculate the index of the uploaded file
                    index = row * cols_per_row + col_index

                    # Check if the index is less than the number of uploaded files
                    if index < len(uploaded_files):

                        # Set the current uploaded file based on the index
                        uploaded_file = uploaded_files[index]

                        # Set the column to display the uploaded image using the current column index
                        with cols[col_index]:
                            # Preprocess the uploaded image
                            image = preprocess_image(uploaded_file, target_size=(96, 96))

                            if image is not None:
                                # Perform prediction
                                predicted_class, confidence = predict(image, model)

                                if predicted_class is not None:
                                    # Display prediction result
                                    st.image(uploaded_file, caption=f'Uploaded Image ({predicted_class}, {confidence:.2f}%)', use_column_width=True)

                                    # Save prediction button with index image            
                                    if st.button(f"Save Prediction {index+1}"):
                                        # Check if the user is authenticated
                                        if 'authenticated' in st.session_state and st.session_state.authenticated:
                                            # Get the user ID
                                            user_id = get_user_id(st.session_state.token)

                                            # Get the current predictions saved of the user
                                            predictions = get_prediction_history(user_id, st.session_state.token)
                                            
                                            # Check if the user has already exceeded the limit of 10 saved predictions
                                            if len(predictions) >= 10:
                                                st.warning('You have reached the limit of 10 saved predictions.')
                                            else:
                                                # Save the prediction
                                                with st.expander("Prediction Status", expanded=True):
                                                    save_prediction(user_id, predicted_class, confidence, uploaded_file, st.session_state.token)
                                        else:
                                            st.warning('Please login to save the prediction.')

# ----------------------------------------------------------------------------------------------------------------

# Main Streamlit app
def main():
    '''
    Main function to run the Streamlit page
    '''
    st.title("Welcome to Deepcatcher Demo")
    selected_option = option_menu(
        menu_title="Main Menu",
        options=["Predict", "History"],
        icons=["camera", "clock"],  # optional
        menu_icon="cast",  # optional
        default_index=0,
        orientation="horizontal", # orientation: horizontal (default) or vertical
    )
    if selected_option == "Predict":
        predict_view()
    elif selected_option == "History":
        history_view()


if __name__ == '__main__':
    main()