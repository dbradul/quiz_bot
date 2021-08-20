import json
import os
import requests

# Endpoints
BASE_API_URL = os.environ.get('API_URL')
# BACKEND_API_TEST = f'{base_api_url}/tests/'
# BACKEND_API_TEST_DETAIL = f'{base_api_url}/tests/' '{0}/'
# BACKEND_API_TEST_RESULT = f'{base_api_url}/tests/' '{0}/results/'
# BACKEND_API_TEST_RESULT_DETAIL = f'{base_api_url}/results/' '{0}/'
# BACKEND_API_TEST_CHOICE_DETAIL = f'{base_api_url}/choices/' '{0}/'
# BACKEND_API_TEST_QUESTION = f'{base_api_url}/tests/' '{0}/questions'
# BACKEND_API_TEST_QUESTION_DETAIL = f'{base_api_url}/tests/' '{0}/questions/' '{1}/'
# BACKEND_API_USER = f'{base_api_url}/users/'


class ApiClient:
    HTTP_OK = 200
    HTTP_OK_CREATE = 201

    METHOD_SUCCESS_CODES = {
        'get': HTTP_OK,
        'post': HTTP_OK_CREATE,
        'patch': HTTP_OK,
    }

    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, method, url, **kwargs):
        request_method = getattr(requests, method)
        params = {'url': url}
        params.update(kwargs)
        response = request_method(**params)
        if response.status_code == self.METHOD_SUCCESS_CODES.get(method, 0):
            return json.loads(response.text)
        raise RuntimeError(f'{method.capitalize()} response: {response.status_code}, {response.reason}')

    def get(self, url):
        return self._request('get', url)

    def post(self, url, payload):
        return self._request('post', url, data=payload)

    def patch(self, url, payload):
        return self._request('patch', url, data=payload)
