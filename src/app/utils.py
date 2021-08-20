import uuid

callback_data_map = {}


def create_callback_data(key, value):
    global callback_data_map
    compound_key = f'{key}_{uuid.uuid4().hex}'
    callback_data_map[compound_key] = value
    return compound_key


def retrieve_callback_data(compound_key):
    return callback_data_map.get(compound_key)
