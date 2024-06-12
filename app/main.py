import streamlit as st
from st_pages import Page, show_pages
from pages.report import main as report_main

st.set_page_config(page_title="Deepcatcher Demo", page_icon=":globe_with_meridians:")

# Set the pages in the sidebar of the app
show_pages(
    [
        Page("main.py", "Home", "🏠"),
        Page("pages/predict.py", "Prediction", "🔮"),
        Page("pages/authenticate.py", "Sign In", "🔒"),
        Page("pages/report.py", "Report", "📝"),
        # Page("pages/information.py", "Information", "📄")
    ]
)

def main():
    st.title("Welcome to Deepcatcher Demo")
    st.write("Deepcatcher is a deep learning model that can classify images as real or fake.")
    st.write("You can use this demo to classify images and view the prediction history.")
    st.write("Please select an option from the sidebar to get started.")

if __name__ == "__main__":
    main()
