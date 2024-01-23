import requests


class APIClient:

    def __init__(self, base_url='http://localhost:9009'):
        self.base_url = base_url

    def status_code_20x(self, status_code):
        return 200 <= status_code < 300

    def api_request(self, path, method, payload=None):
        url = self.base_url + path
        response = requests.request(method, url, json=payload)
        return response.json() if self.status_code_20x(response.status_code) else None
