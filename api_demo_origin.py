import requests


def status_code_20x(status_code):
    return 200 <= status_code < 300


def api_request(url, method, payload=None):
    response = requests.request(method, url, json=payload)
    return response.json() if status_code_20x(response.status_code) else None
