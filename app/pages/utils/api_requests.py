import requests

# ----------------------------------------------------------------------------------------
# Prediction Requests
# ----------------------------------------------------------------------------------------

def get_prediction_history(user_id, token):
    '''
    Function to get request to the API to get the prediction history for a user
    params:
        user_id: User ID
        token: Token of the authenticated user
    '''
    # Set the URL of the API
    url_api = f"http://127.0.0.1:8000/user-service/predictions/?user={user_id}"

    # Set the headers with the token
    headers = {'Authorization': f'Token {token}'}

    # Send the GET request to the API
    response = requests.get(url_api, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return (f"Error at getting predictions history for this user.", 
                f"The Error was: {response.status_code} - {response.json()}")

# ----------------------------------------------------------------------------------------
# User Requests
# ----------------------------------------------------------------------------------------

def get_user_id(token):
    '''
    Function to get the user ID from the API using the token
    params:
        token: Token of the authenticated user
    '''
    # Set the URL of the API
    url_api = "http://127.0.0.1:8000/user-service/user/id/"

    # Set the headers with the token
    headers = {'Authorization': f'Token {token}'}

    # Send the GET request to the API
    response = requests.get(url_api, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json().get('user_id')
    else:
        return ("Error at getting the User ID.")
    
# ----------------------------------------------------------------------------------------
# Report Requests
# ----------------------------------------------------------------------------------------

def get_user_reports(user_id, token):
    '''
    Function to get the reports submitted by a user
    params:
        user_id: The ID of the user
        token: Authentication token
    returns:
        List of reports
    '''
    # Set the URL of the API
    url_api = f'http://127.0.0.1:8000/user-service/reports/user_reports/?user={user_id}'

    # Set the headers with the token
    headers = {'Authorization': f'Token {token}'}

    # Send the GET request to the API
    response = requests.get(url_api, headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        return (f"Error fetching reports: {response.status_code} - {response.json()}")
