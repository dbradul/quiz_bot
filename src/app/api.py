import json
import os
import requests

# Endpoints
BACKEND_API_BASE = os.environ.get('API_URL')
BACKEND_API_TEST = f'{BACKEND_API_BASE}/tests/'
BACKEND_API_TEST_DETAIL = f'{BACKEND_API_BASE}/tests/''{0}/'
BACKEND_API_TEST_RESULT = f'{BACKEND_API_BASE}/tests/''{0}/results/'
BACKEND_API_TEST_RESULT_DETAIL = f'{BACKEND_API_BASE}/results/''{0}/'
BACKEND_API_TEST_CHOICE_DETAIL = f'{BACKEND_API_BASE}/choices/''{0}/'
BACKEND_API_TEST_QUESTION = f'{BACKEND_API_BASE}/tests/''{0}/questions'
BACKEND_API_TEST_QUESTION_DETAIL = f'{BACKEND_API_BASE}/tests/''{0}/questions/''{1}/'
BACKEND_API_USER = f'{BACKEND_API_BASE}/users/'

RESULT_FIELD_QUESTIONS_COUNT = "questions_count"
RESULT_FIELD_CURRENT_ORDER_NUMBER = 'current_order_number'
RESULT_FIELD_TEST = 'test'
USER_FIELD_RATING = 'rating'
USER_FIELD_USERNAME = 'username'

TEST_STATE_FINISHED = 'Finished'

HTTP_OK = 200
HTTP_OK_CREATE = 201

def get_tests():
    url=BACKEND_API_TEST
    response = requests.get(url=url)
    tests = []
    if response.status_code == HTTP_OK:
        tests = json.loads(response.text)
    return tests


def get_test(test_id):
    url=BACKEND_API_TEST_DETAIL.format(test_id)
    response = requests.get(url=url)
    test = None
    if response.status_code == HTTP_OK:
        test = json.loads(response.text)
    return test


def get_test_result(test_result_id):
    url=BACKEND_API_TEST_RESULT_DETAIL.format(test_result_id)
    response = requests.get(url=url)
    test_result = None
    if response.status_code == HTTP_OK:
        test_result = json.loads(response.text)
    return test_result


def create_test_result(test_id):
    url=BACKEND_API_TEST_RESULT.format(test_id)
    response = requests.post(url=url)
    test_result = None
    if response.status_code == HTTP_OK_CREATE:
        test_result = json.loads(response.text)
    return test_result


def update_test_result(test_result_id, payload):
    url=BACKEND_API_TEST_RESULT_DETAIL.format(test_result_id)
    response = requests.patch(url=url, data=payload)
    test_result = None
    if response.status_code == HTTP_OK:
        test_result = json.loads(response.text)
    return test_result


def get_test_questions(test_id):
    url=BACKEND_API_TEST_QUESTION.format(test_id)
    response = requests.get(url=url)
    test_questions = []
    if response.status_code == HTTP_OK:
        test_questions = json.loads(response.text)
    return test_questions


def get_test_question(test_id, order_number):
    url=BACKEND_API_TEST_QUESTION_DETAIL.format(test_id, order_number)
    response = requests.get(url=url)
    question = None
    if response.status_code == HTTP_OK:
        question = json.loads(response.text)
    return question


def get_choice(choice_id):
    url=BACKEND_API_TEST_CHOICE_DETAIL.format(choice_id)
    response = requests.get(url=url)
    choice = None
    if response.status_code == HTTP_OK:
        choice = json.loads(response.text)
    return choice


def get_users():
    url=BACKEND_API_USER
    response = requests.get(url=url)
    users = []
    if response.status_code == HTTP_OK:
        users = json.loads(response.text)
    return users
