import requests


class APIClient:

    def __init__(self, base_url='http://localhost:9009'):
        self.base_url = base_url

    def api_request(self, path, method, payload=None, data=None):
        """
        Sends an API request to the specified path and method.

        Args:
            path (str): The path of the API endpoint.
            method (str): The HTTP method to use for the request.
            payload (dict, optional): The JSON payload for the request.
            data (dict, optional): The data payload for the request.

        Returns:
            requests.Response: The response object.

        Raises:
            ValueError: If the method parameter is not a valid HTTP method.
            requests.exceptions.RequestException: If an error occurs during the API request.
            Exception: If the request fails with a non-successful status code.
        """
        valid_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if method not in valid_methods:
            raise ValueError(f"Invalid method: {method}. Supported methods are: {valid_methods}")
        
        url = self.base_url + path
        try:
            response = requests.request(method, url, json=payload, data=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            return None


class MockService:
    LOGIN_PATH = '/token'
    ITEM_PATH = '/items'

    def __init__(self, user, password):
        self.api_client = APIClient()
        self.auth_token = None
        self.api_login(user, password)

    def api_login(self, user, password):
        if not user or not password:
            raise ValueError("Invalid user or password")

        data = {
            'grant_type': 'password',
            'username': user,
            'password': password
        }
        response = self.api_client.api_request(self.LOGIN_PATH, method='POST', data=data)
        if response and response.status_code == 200:
            self.auth_token = response.json().get('access_token')

    def add_item(self, body):
        if not self.auth_token:
            raise ValueError("auth_token is not set")
        try:
            return self.api_client.api_request(self.ITEM_PATH, method='POST', payload=body)
        except Exception as e:
            raise Exception("Failed to add item: " + str(e))

    def get_item(self, item_id):
        """

        :param item_id:
        :return:
        """
        if not self.auth_token:
            raise ValueError("auth_token is not set")
        if not isinstance(item_id, str):
            raise ValueError("item_id must be a string")
        try:
            return self.api_client.api_request(self.ITEM_PATH + "/" + item_id, method='GET')
        except Exception as e:
            raise Exception("Failed to get item: " + str(e))
