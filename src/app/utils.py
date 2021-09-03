import uuid

from telebot import types

from app.api import NOT_AUTHORIZED_MESSAGE, NotAuthorizedException, BACKEND_AUTHORISE_URL
from app.bot import bot

callback_data_map = {}

# TODO: could be replaced with DB
user_id_map = {}


def create_callback_data(key, value):
    global callback_data_map
    compound_key = f'{key}_{uuid.uuid4().hex}'
    callback_data_map[compound_key] = value
    return compound_key


def retrieve_callback_data(compound_key):
    return callback_data_map.get(compound_key)


def login_required(func):
    """ Decorator """

    def call(message):
        """ Actual wrapping """
        keyboard = types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton(text="Log in Quiz 🔑", url=f"{BACKEND_AUTHORISE_URL}")
        )

        if hasattr(message, 'data'):  # callback
            chat_id = message.message.chat.id
        else:  # command
            chat_id = message.chat.id

        if chat_id not in user_id_map:
            bot.send_message(
                chat_id=chat_id,
                text=NOT_AUTHORIZED_MESSAGE,
                reply_markup=keyboard
            )
            return
        else:
            user = user_id_map[chat_id]
            message.__dict__['user'] = user

        try:
            result = func(message)
            return result
        except NotAuthorizedException:
            bot.send_message(
                chat_id=chat_id,
                text=NOT_AUTHORIZED_MESSAGE,
                reply_markup=keyboard
            )
        except Exception as ex:
            bot.send_message(
                chat_id=chat_id,
                text=f'Something is not quite right :(\n Error details: {ex!r}'
            )

    return call
