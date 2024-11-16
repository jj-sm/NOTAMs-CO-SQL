# Client ID: 7caab856-751b-40d7-ba13-e43da92c5003
# Pass: X8NVLruCcNIIGXmFyqgzSwAMiZex3mof

import requests

# Your client ID and secret
CLIENT_ID = '7caab856-751b-40d7-ba13-e43da92c5003'
CLIENT_SECRET = 'X8NVLruCcNIIGXmFyqgzSwAMiZex3mof'

# The token endpoint for OAuth2 authentication
TOKEN_URL = 'https://api.ivao.aero/oauth/token'

# The NOTAMs endpoint
NOTAMS_URL = 'https://api.ivao.aero/v2/divisions/CO/notams'


# Function to get the access token
def get_access_token(client_id, client_secret):
    # Prepare the headers for the token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")


# Function to fetch the NOTAMs
def get_notams(access_token):
    # Set the authorization header with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send GET request to retrieve the NOTAMs
    response = requests.get(NOTAMS_URL, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the JSON response containing NOTAMs
    else:
        raise Exception(f"Failed to fetch NOTAMs: {response.status_code}, {response.text}")


# Main function
def main():
    try:
        # Get access token
        access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        print("Access token retrieved successfully.")

        # Fetch NOTAMs
        notams = get_notams(access_token)
        print("NOTAMs retrieved successfully.")

        # Print the NOTAMs or handle the data as needed
        print(notams)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
