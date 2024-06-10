import streamlit as st
import requests

def main():
    # Verificar autenticación
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning('Please login to report a prediction.')
        return

    # Obtener predicciones del historial
    user_id = get_user_id(st.session_state.token)
    predictions = get_prediction_history(user_id, st.session_state.token)

    # Parámetro para saber si la vista viene desde un reporte
    prediction_id = st.experimental_get_query_params().get('prediction_id', [None])[0]

    if prediction_id:
        # Mostrar la predicción seleccionada
        prediction = next((p for p in predictions if p['id'] == int(prediction_id)), None)
        if prediction:
            st.subheader("Selected Prediction")
            st.image(prediction['image'], caption=f"{prediction['predicted_class']} - {prediction['confidence']:.2f}%")
            st.write(f"Prediction made on {prediction['timestamp']}")
    else:
        # Mostrar un selector para elegir una predicción
        st.subheader("Select a Prediction to Report")
        prediction_options = {f"{p['predicted_class']} - {p['timestamp']}": p['id'] for p in predictions}
        selected_prediction = st.selectbox("Choose a prediction", options=list(prediction_options.keys()))
        prediction_id = prediction_options[selected_prediction]

    # Formulario de reporte
    st.subheader("Report Prediction")
    title = st.text_input("Title")
    description = st.text_area("Description")
    feedback = st.text_area("Feedback")

    if st.button("Submit Report"):
        # Enviar el reporte a la API
        data = {
            "title": title,
            "description": description,
            "prediction": prediction_id,
            "feedback": feedback
        }
        headers = {'Authorization': f'Token {st.session_state.token}'}
        response = requests.post('http://127.0.0.1:8000/user-service/reports/', headers=headers, data=data)
        if response.status_code == 201:
            st.success("Report successfully submitted.")
        else:
            st.error(f"Error submitting the report: {response.status_code} - {response.json()}")

def get_user_id(token):
    # Implementar la función para obtener el ID del usuario autenticado
    pass

def get_prediction_history(user_id, token):
    # Implementar la función para obtener el historial de predicciones del usuario
    pass

if __name__ == "__main__":
    main()
