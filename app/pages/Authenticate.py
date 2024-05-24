import streamlit as st
import requests

# Simulación de autenticación simple
def authenticate(username, password):
    url_api = "http://127.0.0.1:8000/user-service/users/authenticate/"
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url_api, data=data)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        st.error("Error de autenticación")

# Variable para almacenar el estado de autenticación
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'token' not in st.session_state:
    st.session_state.token = None

# Formulario de inicio de sesión
if not st.session_state.authenticated:
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        token = authenticate(username, password)
        if token:
            print("Este es el token", token)
            st.session_state.token = token
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Inicio de sesión fallido")

# Contenido visible solo si está autenticado
if st.session_state.authenticated:
    st.success("¡Has iniciado sesión!")
    st.write("Contenido exclusivo para usuarios autenticados.")

    st.write("Token de autenticación:", st.session_state.token)
    
    # Aquí puedes agregar tu historial de uso de la aplicación
    st.subheader("Historial de uso de la aplicación")
    st.write("Aquí va tu historial de uso...")

else:
    st.warning("Debes iniciar sesión para ver el contenido exclusivo.")
    st.write("Contenido público visible para todos.")

# Opción para cerrar sesión
if st.session_state.authenticated:
    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.token = None
        st.experimental_rerun()
