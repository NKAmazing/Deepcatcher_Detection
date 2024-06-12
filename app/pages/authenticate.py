import streamlit as st
import requests
from streamlit_option_menu import option_menu
from pages.utils.helpers import capitalize_first

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
    '''
    url_api = "http://127.0.0.1:8000/user-service/users/authenticate/"
    data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url_api, data=data)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            st.error("Error de autenticación.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None
    
# Registration function
def register(username, email, password):
    '''
    Function to register a new user trough a POST request to the API
    '''
    url_api = "http://127.0.0.1:8000/user-service/users/"
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    try:
        response = requests.post(url_api, data=data)
        if response.status_code == 201:
            return response.json().get('username')
        elif response.status_code == 400:
            error_message = parse_error_message(response)
            st.error(f"Error de registro de usuario: {error_message}")
        else:
            st.error("Error de registro de usuario.")
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None
    
def parse_error_message(response):
    '''
    Function to parse the error message from the response
    '''
    try:
        error_data = response.json()
        if 'email' in error_data:
            return capitalize_first(error_data['email'][0])
        elif 'username' in error_data:
            return capitalize_first(error_data['username'][0])
        else:
            return "Error desconocido al registrar usuario."
    except:
        return "Error desconocido al registrar usuario."

# Login view in the page
def login_view():
    '''
    View for the login page
    '''
    st.title("Sign In")
    if not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            token = authenticate(username, password)
            if token:
                st.session_state.username = capitalize_first(username)
                st.session_state.token = token
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Sign In failed")
    else:
        st.success("You have signed in!")
        st.write(f"Welcome back {st.session_state.username}!")
        if st.button("Cerrar sesión"):
            st.session_state.authenticated = False
            st.session_state.token = None
            st.experimental_rerun()

# Register view in the page
def register_view():
    '''
    View for the register page
    '''
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        response = register(username, email, password)
        if response:
            st.session_state.username = capitalize_first(username)
            st.session_state.authenticated = True
            st.success("You have signed up successfully!")
            st.success(f"You have automatically logged in. Welcome {st.session_state.username}!")
        else:
            st.error("Sign Up failed")

# Main function of the authenticate page
def main():
    '''
    Main function of the authenticate page
    '''
    selected_option = option_menu(
        menu_title="User Authentication",
        options=["Sign In", "Sign Up"],
        icons=["sign-in", "user-add"],
        menu_icon="lock",
        default_index=0,
        orientation="horizontal", # orientation: horizontal (default) or vertical
    )
    if selected_option == "Sign In":
        login_view()
    elif selected_option == "Sign Up":
        register_view()

if __name__ == '__main__':
    main()