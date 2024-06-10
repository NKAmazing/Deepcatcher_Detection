import streamlit as st
from streamlit_option_menu import option_menu
import requests
# from pages.Authenticate import show_login, show_authenticated_content
from st_pages import Page, show_pages

st.set_page_config(page_title="Deepcatcher Demo", page_icon=":globe_with_meridians:", layout="wide", initial_sidebar_state="expanded")

# st.title("Deepcatcher Demo")

# st.write("Welcome to Deepcatcher, an image detection app for fake images.")

st.sidebar.title("Deepcatcher Demo")

options = st.sidebar.radio("Select an option: ", ["Home"])

# Set the pages in the sidepar of the app
show_pages(
    [
        Page("main.py", "Home", "🏠"),
        Page("pages/predict.py", "Prediction", "🔮"),
        # Page("pages/authenticate.py", "Login/Register", "📝"),
        # Page("pages/report.py", "Report", "📊"),
        # Page("pages/information.py", "Information", "📄")
    ]
)

def home_view():
    st.title("Welcome to Deepcatcher Demo")
    st.write("Deepcatcher is a deep learning model that can classify images as real or fake.")
    st.write("You can use this demo to classify images and view the prediction history.")
    st.write("Please select an option from the sidebar to get started.")


def main():
    if options == "Home":
        home_view()
    else:
        st.write("Select an option from the sidebar to get started.")

if __name__ == "__main__":
    main()