import streamlit as st
import requests
from streamlit_option_menu import option_menu
from pages.utils.helpers import capitalize_first

st.set_page_config(page_title="Deepcatcher Demo - User Authentication", page_icon=":lock:")

# Variable to store the authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Variable to store the token
if 'token' not in st.session_state:
    st.session_state.token = None

# Authentication function
def authenticate(username, password):
    '''
    Function to authenticate a user trough a POST request to the API
    params:
        username: The username of the user (string)
        password: The password of the user (string)
    '''
    # Set the URL of the API
    url_api = "http://127.0.0.1:8000/user-service/users/authenticate/"

    # Set the data to be sent in the POST request
    data = {
        'username': username,
        'password': password
    }
    try:
        # Send the POST request to the API
        response = requests.post(url_api, data=data)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json().get('token')
        else:
            st.error("Authentication Error.")
    except Exception as e:
        # Handle connection errors
        st.error(f"Connection Error: {e}")
        return None
    
# Registration function
def register(username, email, password):
    '''
    Function to register a new user trough a POST request to the API
    '''
    # Set the URL of the API
    url_api = "http://127.0.0.1:8000/user-service/users/"

    # Set the data to be sent in the POST request
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    try:
        # Send the POST request to the API
        response = requests.post(url_api, data=data)
        # Check the status code of the response
        if response.status_code == 201:
            # If the response is successful, return the response data
            response_data = response.json()
            return response_data
        elif response.status_code == 400:
            # If the response is a bad request, parse the error message
            error_message = parse_error_message(response)
            st.error(f"User Registration Error: {error_message}")
        else:
            st.error("User Registration Error.")
    except Exception as e:
        # Handle connection errors
        st.error(f"Connection Error: {e}")
        return None
    
def parse_error_message(response):
    '''
    Function to parse the error message from the response
    '''
    try:
        # Parse the error message from the response
        error_data = response.json()

        # Check if the error message contains the 'email' or 'username' key
        if 'email' in error_data:
            return capitalize_first(error_data['email'][0])
        elif 'username' in error_data:
            return capitalize_first(error_data['username'][0])
        else:
            return "Unknown error while registering user."
    except:
        return "Unknown error while registering user."

# Login view in the page
def login_view():
    '''
    View for the login page
    '''
    st.title("Sign In")

    # If the user is not authenticated, show the login form
    if not st.session_state.authenticated:
        # Input fields for the login form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Button to submit the login form
        if st.button("Sign In"):
            # Call the authenticate function to log in the user
            token = authenticate(username, password)

            # Check if the authentication was successful
            if token:
                # Set the session state variables
                st.session_state.username = capitalize_first(username)
                st.session_state.token = token
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Sign In failed")
    else:
        # If the user is already authenticated, show a welcome message
        st.success("You have signed in!")
        st.write(f"Welcome back {st.session_state.username}!")

        # Button to log out
        if st.button("Log Out"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.experimental_rerun()

# Register view in the page
def register_view():
    '''
    View for the register page
    '''
    st.title("Sign Up")

    # Input fields for the registration form
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    repeat_password = st.text_input("Repeat Password", type="password")

    # Button to submit the registration form
    if st.button("Sign Up"):

        # Check if the passwords match
        if password == repeat_password and password != "":

            # Call the register function to create a new user
            response = register(username, email, password)

            # Check if the registration was successful
            if response:
                # Set the session state variables
                st.session_state.username = capitalize_first(username)
                st.session_state.authenticated = True
                st.session_state.token = response.get('token')
                st.success("You have signed up successfully!")
                st.success(f"You have automatically logged in. Welcome {st.session_state.username}!")
            else:
                st.error("Sign Up failed")
        elif password != repeat_password:
            # Show an error message if the passwords do not match
            st.error("Passwords do not match.")

# Main function of the authenticate page
def main():
    '''
    Main function of the authenticate page
    '''
    # Show the user authentication menu
    selected_option = option_menu(
        menu_title="User Authentication",
        options=["Sign In", "Sign Up"],
        icons=["sign-in", "user-add"],
        menu_icon="lock",
        default_index=0,
        orientation="horizontal", # orientation: horizontal (default) or vertical
    )
    # Check the selected option
    if selected_option == "Sign In":
        login_view()
    elif selected_option == "Sign Up":
        register_view()

if __name__ == '__main__':
    main()