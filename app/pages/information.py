import streamlit as st

# Set the page configuration
st.set_page_config(page_title="About Deepcatcher", page_icon="📄", initial_sidebar_state="expanded", layout="wide")

def about():
    st.title("About Deepcatcher")

    # Add information about the app and the project through a markdown
    st.markdown(
        """
        ## Abstract
        **Deepcatcher** is a software solution designed to detect images manipulated with Artificial Intelligence, commonly referred to as Deepfakes. The application employs a robust Machine Learning model to provide accurate predictions of image authenticity. Users interact with Deepcatcher through a responsive web interface, where they can upload images for analysis.

        The application also incorporates a user registration system, enabling users to log in, save their prediction results, and submit feedback or reports on the predictions made. This comprehensive approach ensures not only high accuracy in detecting fake images but also a user-friendly experience that facilitates ongoing interaction and improvement through user feedback. The combination of advanced AI techniques and a simplified web interface positions Deepcatcher as a valuable tool in the fight against digital image manipulation.

        ## Architecture

        #### Detection Model
        - **Model Training**: The detection model is trained in a Python Notebook using TensorFlow, where a series of controlled steps are taken to train the deepfake detector.
        - **Direct Connection**: The detection model is loaded through a direct connection between the Frontend service and the model service. This is facilitated by TensorFlow tools that allow quick loading of a model in a Python script.

        #### Backend
        - **REST API with Django**: The Backend is built using the Django framework, providing a RESTful API to manage the main functionalities of the application.
        - **User Registration Tool**: Allows the creation and management of user accounts.
        - **Prediction History Tool**: Records and allows the consultation of predictions made by users.
        - **User Reporting Tool**: Users can make reports related to the predictions or any other aspect of the application.
        - **SQL Database**: User data, predictions, and reports are stored in an SQL database, ensuring data persistence and accessibility.

        #### Frontend
        - **Multi-page Interface with Streamlit**: The Frontend is developed with the Streamlit framework, which allows the rapid and easy creation of web interfaces.
            - **File Management Microservice**: Facilitates the management of files that users upload for predictions.
            - **Deepcatcher Web Pages**: Provide the user interface to interact with the various functionalities of the application, such as uploading files for detection, viewing prediction history, and reports.

        ## Credits
        - **Developer**: [Nicolas Mayoral](https://github.com/NKAmazing), student at the Faculty of Engineering, Universidad de Mendoza
        - **Specialist Tutor in Charge**: Mariela Asensio
        - **University**: Universidad de Mendoza
        """
    )

if __name__ == "__main__":
    about()
