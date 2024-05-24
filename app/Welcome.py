import streamlit as st
from streamlit_option_menu import option_menu
import requests

st.set_page_config(page_title="Deepcatcher Demo", page_icon=":globe_with_meridians:")

st.title("Deepcatcher Demo")

st.write("Bienvenido a Deepcatcher, una aplicación de detección de imágenes fakes.")

st.sidebar.title("Menú")

menu = st.sidebar.radio("Selecciona una opción", ["Inicio", "Registro", "Login"])

if 'token' not in st.session_state:
    st.session_state.token = None

def get_user_id(token):
    url_api = "http://127.0.0.1:8000/user-service/user/id/"
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(url_api, headers=headers)
    if response.status_code == 200:
        return response.json().get('user_id')
    else:
        st.error("Error al obtener el ID del usuario")
        return None


if menu == "Inicio":
    st.write("Aquí va el contenido de la página de inicio")
    # Configurar el menú de navegación
    selected = option_menu(
        menu_title=None,  # required
        options=["Inicio", "Historial"],  # required
        icons=["house", "person-add"],  # optional
        menu_icon="cast",  # optional
        default_index=0,  # optional
        orientation="horizontal",
    )

    # Actualizar la página según la selección en el menú
    if selected == "Inicio":
        st.session_state.page = "inicio"
    elif selected == "Historial":
        st.session_state.page = "historial"

    # Configurar las rutas basadas en el estado de la página
    if st.session_state.page == "inicio":
        st.title("Página de Inicio")
        st.write("Bienvenido a la página de inicio.")
        st.write(st.session_state.token)
        
        # Get the user_id through a button
        if st.button("Obtener ID de Usuario"):
            user_id = get_user_id(st.session_state.token)
            st.write(f"ID de Usuario: {user_id}")

    elif st.session_state.page == "historial":
        st.title("Historial de Uso")
        st.write("Aquí se mostrará el historial de uso de la aplicación.")
elif menu == "Registro":
    st.title("Formulario de Registro")

    username = st.text_input("Nombre de Usuario")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrarse"):
        if not username or not email or not password:
            st.error("Todos los campos son obligatorios")
        else:
            response = requests.post("http://127.0.0.1:8000/user-service/users/", data={
                'username': username,
                'password': password,
                'email': email   
            })
            
            if response.status_code == 201:
                st.success("Usuario registrado con éxito")
            else:
                try:
                    error_message = response.json().get('error')
                except ValueError:  # incluye JSONDecodeError
                    error_message = "Error inesperado: respuesta no válida del servidor"
                st.error(error_message)
else:
    st.title("Formulario de Login")

    username = st.text_input("Nombre de Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        if not username or not password:
            st.error("Todos los campos son obligatorios")
        else:
            response = requests.post("http://localhost:8000/api/login/", data={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                st.success("Inicio de sesión exitoso")
            else:
                try:
                    error_message = response.json().get('error')
                except ValueError:  # incluye JSONDecodeError
                    error_message = "Error inesperado: respuesta no válida del servidor"
                st.error(error_message)
