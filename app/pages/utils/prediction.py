import tensorflow as tf

# Function to load the model
def load_model(model_path):
    '''
    Function to load the model
    params:
        model_path: Path to the model
    '''
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        return (f"Model Load Error: {str(e)}")

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
        return (f"Prediction Error: {str(e)}")
    
# # Model paths
# model_paths = ['../detection_model/models/model_0.h5', '../detection_model/models/model_1.h5', 
#                '../detection_model/models/model_2.h5', '../detection_model/models/model_3.h5',
#                '../detection_model/models/model_4.h5']

# # Load the model
# model = tf.keras.models.load_model(model_paths[4])