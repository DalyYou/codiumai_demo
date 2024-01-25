import requests


class APIClient:

    def __init__(self, base_url='http://localhost:9009'):
        self.base_url = base_url

    def api_request(self, path, method, payload=None, data=None):
        url = self.base_url + path
        return requests.request(method, url, json=payload, data=data)


class MockService:
    LOGIN_PATH = '/token'
    ITEM_PATH = '/items'

    def __init__(self, user, password):
        self.api_client = APIClient()
        self.api_login(user, password)

    def api_login(self, user, password):
        data = {
            'grant_type': 'password',
            'username': user,
            'password': password
        }
        return self.api_client.api_request(self.LOGIN_PATH, method='POST', data=data)

    def add_item(self, body):
        return self.api_client.api_request(self.ITEM_PATH, method='POST', payload=body)

    def get_item(self, item_id):
        return self.api_client.api_request(self.ITEM_PATH + "/" + item_id, method='GET')


# S1
s1 = MockService('user1', 'secret1')
s1_res1 = s1.add_item({
    "item_id": 1,
    "item_name": "item name"
})
assert s1_res1.status_code == 201

s1_res2 = s1.get_item("1")
assert s1_res2.status_code == 200
