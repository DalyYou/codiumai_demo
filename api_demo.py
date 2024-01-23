import urllib.parse
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RequestException
from urllib3.util.retry import Retry
import logging
import requests


class APIClient:

    def __init__(self, base_url='http://localhost:9009'):
        self.base_url = base_url
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.response_handlers = {
            'raw': None,
            'text': None,
            'json': None
        }

    def status_code_20x(self, status_code: int) -> bool:
        """
        Check if the status code is in the 20x range.

        Args:
            status_code (int): The status code to check.

        Returns:
            bool: True if the status code is in the 20x range, False otherwise.
        """
        return 200 <= status_code < 300

    def api_request(self, path, method='GET', payload=None, headers=None, data=None, params=None, auth=None,
                    proxies=None,
                    cookies=None, files=None, allow_redirects=True, stream=False, verify=True, response_type='json',
                    status_code=200, timeout=5):
        """
        Make an API request.

        Args:
            path (str): The URL to make the request to.
            method (str, optional): The HTTP method to use. Defaults to 'GET'.
            payload (dict, optional): The JSON payload to send with the request. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.
            data (str, optional): The data to send with the request when the payload is not JSON. Defaults to None.
            params (dict, optional): The query parameters to include in the request when the method is 'GET'. Defaults to None.
            auth (tuple, optional): The authentication credentials to use. Defaults to None.
            proxies (dict, optional): The proxies to use for the request. Defaults to None.
            cookies (dict, optional): The cookies to include in the request. Defaults to None.
            files (dict, optional): The files to upload with the request when the method is 'POST' or 'PUT'. Defaults to None.
            allow_redirects (bool, optional): Whether or not to follow redirects. Defaults to True.
            stream (bool, optional): Whether or not to stream the response. Defaults to False.
            verify (bool, optional): Whether or not to verify SSL certificates. Defaults to True.
            response_type (str, optional): The type of response to return. Defaults to 'json'.
            status_code (int, optional): The expected status code for a successful response. Defaults to 200.
            timeout (int, optional): The timeout value for the request in seconds. Defaults to 5.

        Returns:
            dict or str or None: The response content, or None if the request failed.
        """
        url = urllib.parse.urljoin(self.base_url, path)
        logging.info(f"Making {method} request to {url}")
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=payload,
                headers=headers,
                data=data,
                params=params,
                auth=auth,
                proxies=proxies,
                cookies=cookies,
                files=files,
                allow_redirects=allow_redirects,
                stream=stream,
                verify=verify,
                timeout=timeout
            )
            if status_code is not None and response.status_code != status_code:
                raise HTTPError(f"API request failed with status code {response.status_code}")
            if self.status_code_20x(response.status_code):
                self.response_handlers['raw'] = response
                self.response_handlers['text'] = response.text
                if response.headers.get('content-type') == 'application/json':
                    self.response_handlers['json'] = response.json()
                else:
                    self.response_handlers['json'] = None
            else:
                self.response_handlers['raw'] = None
                self.response_handlers['text'] = None
                self.response_handlers['json'] = None
            return self.response_handlers.get(response_type, None)
        except RequestException as e:
            logging.error(f"An error occurred: {str(e)}")
            raise e


LOGIN_PATH = '/token'

api_client = APIClient()


def api_login(user, password):
    data = {
        'grant_type': 'password',
        'username': user,
        'password': password
    }
    return api_client.api_request(LOGIN_PATH, method='POST', data=data)


aa = api_login('user1', 'secret1')
print(aa)
