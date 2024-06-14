import streamlit as st
from st_pages import Page, show_pages

# Set the page configuration
st.set_page_config(page_title="Deepcatcher Demo - Home", page_icon=":globe_with_meridians:", initial_sidebar_state="expanded", layout="wide")

# Set the pages in the sidebar of the app
show_pages(
    [
        Page("main.py", "Home", "🏠"),
        Page("pages/predict.py", "Prediction", "💻"),
        Page("pages/authenticate.py", "User Authentication", "🔒"),
        Page("pages/report.py", "Report", "📝"),
        Page("pages/information.py", "About", "📄"),
    ]
)

def main():
    # Set the title of the app
    st.title("Welcome to Deepcatcher Demo!") 

    # Adjust the size of the image and center it
    st.markdown(
        """
        <style>
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Create columns to center the image
    left_co, cent_co, last_co = st.columns(3)

    # Display the Deepcatcher image centered
    with cent_co:
        st.image("pages/media/images/Deepcatcher.png", width=500, caption="Deepcatcher - Deepfake Detection App")

    # Add information about the app through a markdown
    st.markdown(
        """
        <div style="text-align: center;">
            <h2>Deepfake Detection App</h2>
            <p>Deepcatcher is a machine learning model designed to classify images as real or fake. This application leverages advanced deep learning techniques to identify deepfakes with high accuracy.</p>
        </div>
        <hr style="border-top: 3px solid #bbb;">
        <div style="text-align: left; margin-left: 15%;">
            <h3>Features:</h3>
            <ul>
                <li><strong>Real-time Prediction:</strong> Upload an image and get instant feedback on its authenticity.</li>
                <li><strong>User Authentication:</strong> Secure your account and keep track of your prediction history.</li>
                <li><strong>Report Generation:</strong> Create and view reports based on the predictions.</li>
            </ul>
            <h3>Get Started</h3>
            <p>Use the sidebar to navigate through the different sections of the app:</p>
            <ul>
                <li><strong>Prediction:</strong> Upload an image and get a prediction.</li>
                <li><strong>User Authentication:</strong> Log in or sign up to save your prediction history.</li>
                <li><strong>Report:</strong> View and manage reports on the predictions you have made.</li>
            </ul>
        </div>
        <hr style="border-top: 3px solid #bbb;">
        <div style="text-align: center;">
            <p>We hope you find Deepcatcher useful for your needs. If you have any feedback or questions, feel free to reach out!</p>
        </div>
        """, unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
