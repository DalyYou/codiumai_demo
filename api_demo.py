from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RequestException
from urllib3.util.retry import Retry
import logging
import requests


def status_code_20x(status_code: int) -> bool:
    """
    Check if the status code is in the 20x range.

    Args:
        status_code (int): The status code to check.

    Returns:
        bool: True if the status code is in the 20x range, False otherwise.
    """
    return 200 <= status_code < 300


def api_request(url, method='GET', payload=None, headers=None, data=None, params=None, auth=None, proxies=None,
                cookies=None, files=None, allow_redirects=True, stream=False, verify=True, response_type='json',
                status_code=None, timeout=5):
    """
    Make an API request.

    Args:
        url (str): The URL to make the request to.
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
        status_code (int, optional): The expected status code for a successful response. Defaults to None.
        timeout (int, optional): The timeout value for the request in seconds. Defaults to 5.

    Returns:
        dict or str or None: The response content, or None if the request failed.
    """
    logging.info(f"Making {method} request to {url}")
    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.request(
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
        response_handlers = {
            'raw': response,
            'text': response.text,
            'json': response.json() if response.headers.get('content-type') == 'application/json' else None
        }
        return response_handlers.get(response_type, None)
    except RequestException as e:
        logging.error(f"An error occurred: {str(e)}")
        raise e
