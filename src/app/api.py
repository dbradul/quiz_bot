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


# HTTP_OK = 200
# HTTP_OK_CREATE = 201


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
        # response = requests.get(url=url)
        # if response.status_code == HTTP_OK:
        #     return json.loads(response.text)
        # raise RuntimeError(f'Get response: {response.status_code}')

    def post(self, url, payload):
        return self._request('post', url, data=payload)
        # response = requests.post(url=url, data=payload)
        # if response.status_code == HTTP_OK_CREATE:
        #     return json.loads(response.text)
        # raise RuntimeError(f'Post response: {response.status_code}')

    def patch(self, url, payload):
        return self._request('patch', url, data=payload)
        # response = requests.patch(url=url, data=payload)
        # if response.status_code == HTTP_OK_CREATE:
        #     return json.loads(response.text)
        # raise RuntimeError(f'Post response: {response.status_code}')


# def get_tests():
#     url=BACKEND_API_TEST
#     response = requests.get(url=url)
#     tests = []
#     if response.status_code == HTTP_OK:
#         tests = json.loads(response.text)
#     return tests
#
#
# def get_test(test_id):
#     url=BACKEND_API_TEST_DETAIL.format(test_id)
#     response = requests.get(url=url)
#     test = None
#     if response.status_code == HTTP_OK:
#         test = json.loads(response.text)
#     return test
#
#
# def get_test_result(test_result_id):
#     url=BACKEND_API_TEST_RESULT_DETAIL.format(test_result_id)
#     response = requests.get(url=url)
#     test_result = None
#     if response.status_code == HTTP_OK:
#         test_result = json.loads(response.text)
#     return test_result
#
#
# def create_test_result(test_id):
#     url=BACKEND_API_TEST_RESULT.format(test_id)
#     response = requests.post(url=url)
#     test_result = None
#     if response.status_code == HTTP_OK_CREATE:
#         test_result = json.loads(response.text)
#     return test_result
#
#
# def update_test_result(test_result_id, payload):
#     url=BACKEND_API_TEST_RESULT_DETAIL.format(test_result_id)
#     response = requests.patch(url=url, data=payload)
#     test_result = None
#     if response.status_code == HTTP_OK:
#         test_result = json.loads(response.text)
#     return test_result
#
#
# def get_test_questions(test_id):
#     url=BACKEND_API_TEST_QUESTION.format(test_id)
#     response = requests.get(url=url)
#     test_questions = []
#     if response.status_code == HTTP_OK:
#         test_questions = json.loads(response.text)
#     return test_questions
#
#
# def get_test_question(test_id, order_number):
#     url=BACKEND_API_TEST_QUESTION_DETAIL.format(test_id, order_number)
#     response = requests.get(url=url)
#     question = None
#     if response.status_code == HTTP_OK:
#         question = json.loads(response.text)
#     return question
#
#
# def get_choice(choice_id):
#     url=BACKEND_API_TEST_CHOICE_DETAIL.format(choice_id)
#     response = requests.get(url=url)
#     choice = None
#     if response.status_code == HTTP_OK:
#         choice = json.loads(response.text)
#     return choice
#
#
# def get_users():
#     url=BACKEND_API_USER
#     response = requests.get(url=url)
#     users = []
#     if response.status_code == HTTP_OK:
#         users = json.loads(response.text)
#     return users
