import streamlit as st
from streamlit_option_menu import option_menu
import requests

st.set_page_config(page_title="Deepcatcher Demo", page_icon=":globe_with_meridians:")

st.title("Deepcatcher Demo")

st.write("Bienvenido a Deepcatcher, una aplicación de detección de imágenes fakes.")

st.sidebar.title("Menú")

menu = st.sidebar.radio("Selecciona una opción", ["Inicio", "Registro", "Login"])

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
            response = requests.post("http://localhost:8000/api/register/", data={
                'username': username,
                'email': email,
                'password': password
            })
            
            if response.status_code == 201:
                st.success("Usuario registrado con éxito")
            else:
                st.error(response.json().get('error'))
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
                st.error(response.json().get('error'))