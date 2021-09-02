import json
import os
import requests

BASE_BACKEND_URL = os.environ.get('BASE_BACKEND_URL')
BASE_API_URL = f'{BASE_BACKEND_URL}/api/v1'
BACKEND_AUTHORISE_URL = f'{BASE_BACKEND_URL}/api/v1/tg_introduce/'
NOT_AUTHORIZED_MESSAGE = "I don't know who you are :( Please, introduce yourself."


class NotAuthorizedException(Exception):
    pass


class ApiClient:
    HTTP_OK = 200
    HTTP_OK_CREATE = 201
    HTTP_UNAUTHORIZED = 401

    METHOD_SUCCESS_CODES = {
        'get': HTTP_OK,
        'post': HTTP_OK_CREATE,
        'patch': HTTP_OK,
    }

    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, method, url, **kwargs):
        request_method = getattr(requests, method)
        params = self.get_params(url, **kwargs)
        response = request_method(**params)
        if response.status_code == self.METHOD_SUCCESS_CODES.get(method, 0):
            return json.loads(response.text)
        elif response.status_code == self.HTTP_UNAUTHORIZED:
            raise NotAuthorizedException()
        raise RuntimeError(f'{method.capitalize()} response: {response.status_code}, {response.reason}')

    def get_params(self, url, **kwargs):
        params = {'url': url}
        params.update(kwargs)
        return params

    def get_url(self, path):
        return f'{self.base_url}/{path}'

    def get(self, url=None, path=None):
        assert not url or not path, "One of the parameters 'url' or 'path' should be passed"
        if url is None:
            url = self.get_url(path)
        return self._request('get', url)

    def post(self, url, payload):
        return self._request('post', url, data=payload)

    def patch(self, url, payload):
        return self._request('patch', url, data=payload)


class JWTApiClient(ApiClient):
    def __init__(self, base_url, jwt_token):
        super().__init__(base_url)
        self.jwt_token = jwt_token

    def get_params(self, url, **kwargs):
        params = super().get_params(url, **kwargs)
        auth_header = {'Authorization': f'Bearer {self.jwt_token}'}
        headers = {'headers': auth_header}
        params.update(headers)
        return params

