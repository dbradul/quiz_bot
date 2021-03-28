import json


def create_question_callback_data(choice, test_result):
    return f'''{{"choice_id": {choice.get('id')}, "test_result_id": {test_result.get('id')}}}'''

def create_test_callback_data(test):
    return f'{{"test_id": {test.get("id")}}}'

def parse_question_callback_data(callback_data):
    choice_id = json.loads(callback_data).get('choice_id')
    test_result_id = json.loads(callback_data).get('test_result_id')
    return choice_id, test_result_id

def parse_test_callback_data(callback_data):
    test_id = json.loads(callback_data).get('test_id')
    return test_id

