import streamlit as st
from streamlit_option_menu import option_menu
from st_pages import Page, show_pages

st.set_page_config(page_title="Deepcatcher Demo", page_icon=":globe_with_meridians:")

st.sidebar.title("Deepcatcher Demo")

# Set the pages in the sidebar of the app
show_pages(
    [
        Page("main.py", "Home", "🏠"),
        Page("pages/predict.py", "Prediction", "🔮"),
        Page("pages/authenticate.py", "Authenticate", "🔒"),
        Page("pages/report.py", "Report", "📝"),
        # Page("pages/information.py", "Information", "📄")
    ]
)

def home_view():
    st.title("Welcome to Deepcatcher Demo")
    st.write("Deepcatcher is a deep learning model that can classify images as real or fake.")
    st.write("You can use this demo to classify images and view the prediction history.")
    st.write("Please select an option from the sidebar to get started.")

def main():
    st.sidebar.selectbox(
        "Go to",
        ["Home", "Prediction", "Authenticate", "Report"],
        key="selected_page"
    )
    selected_page = st.session_state.selected_page

    if selected_page == "Home":
        home_view()
    elif selected_page == "Prediction":
        st.experimental_set_query_params(page="Prediction")
        st.experimental_rerun()
    elif selected_page == "Authenticate":
        st.experimental_set_query_params(page="Authenticate")
        st.experimental_rerun()
    elif selected_page == "Report":
        st.experimental_set_query_params(page="Report")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
