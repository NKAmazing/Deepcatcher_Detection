import streamlit as st
import requests
from pages.utils.api_requests import get_user_id, get_prediction_history, get_user_reports
from streamlit_option_menu import option_menu

# Set the page configuration
st.set_page_config(page_title="Deepcatcher Demo - Home", page_icon=":clipboard:")

def report_view():
    # Verify user authentication
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning('Please login to report a prediction.')
        return

    # Get the user ID
    user_id = get_user_id(st.session_state.token)

    # Get the prediction history for the user
    predictions = get_prediction_history(user_id, st.session_state.token)

    # Analize if there are predictions to show
    if not predictions:
        st.info("No predictions found. Please make a prediction first.")
        return

    # Show a select box to choose a prediction
    st.subheader("Select a Prediction to Report")
    prediction_options = {f"{p['predicted_class']} - {p['timestamp'].split('T')[0]} at {p['timestamp'].split('T')[1].split('.')[0]}": p['id'] for p in predictions}
    selected_prediction = st.selectbox("Choose a prediction", options=list(prediction_options.keys()))
    prediction_id = prediction_options[selected_prediction]

    # Show the selected prediction
    prediction = next((p for p in predictions if p['id'] == int(prediction_id)), None)
    if prediction:
        st.subheader("Selected Prediction")
        st.image(prediction['image'], caption=f"{prediction['predicted_class']} - {prediction['confidence']:.2f}%")
        st.write(f"Prediction made on {prediction['timestamp'].split('T')[0]} at {prediction['timestamp'].split('T')[1].split('.')[0]}")

    # Report form
    st.subheader("Report Prediction")
    title = st.text_input("Title")
    description = st.text_area("Description")

    # If the user submits the report
    if st.button("Submit Report"):
        # Enviar el reporte a la API
        data = {
            "title": title,
            "description": description,
            "prediction": prediction_id,
            "user": user_id
        }
        headers = {'Authorization': f'Token {st.session_state.token}'}
        response = requests.post('http://127.0.0.1:8000/user-service/reports/', headers=headers, data=data)
        if response.status_code == 201:
            st.success("Report successfully submitted.")
        else:
            st.error(f"Error submitting the report: {response.status_code} - {response.json()}")

def reports_history_view():
    # Verificar autenticación
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        st.warning('Please login to view report history.')
        return

    # Obtener reportes del usuario
    user_id = get_user_id(st.session_state.token)
    reports = get_user_reports(user_id, st.session_state.token)

    if reports:
        st.subheader("Reports History")
        for report in reports:
            status_color = "yellow" if report['status'] == 'Pending' else "green"
            with st.expander(f"Report: {report['title']} - {report['timestamp'].split('T')[0]} at {report['timestamp'].split('T')[1].split('.')[0]}"):
                st.write(f"**Title:** {report['title']}")
                st.write(f"**Description:** {report['description']}")
                st.write(f"**Reported on:** {report['timestamp'].split('T')[0]} at {report['timestamp'].split('T')[1].split('.')[0]}")
                st.markdown(f"**Status:** <span style='color:{status_color}'>**{report['status']}**</span>", unsafe_allow_html=True)
    else:
        st.info("No reports found.")

def main():
    '''
    Main function to display the report page
    '''
    selected_option = option_menu(
        menu_title="Reports and Application Support",
        options=["Report Prediction", "Reports History"],
        icons=["📝", "📄"],
        menu_icon="clipboard",
        default_index=0,
        orientation="horizontal"
    )
    if selected_option == "Report Prediction":
        report_view()
    else:
        reports_history_view()

if __name__ == "__main__":
    main()
