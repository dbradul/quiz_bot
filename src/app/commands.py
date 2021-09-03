import re
from enum import Enum

import telebot

from app.api import BASE_API_URL, ApiClient
from app.utils import user_id_map, login_required
from app.fetchers import TestModelFetcher, UserModelFetcher
from app.bot import bot
from app.services import TestRunner
from app.models import User
from app.utils import (
    retrieve_callback_data,
    create_callback_data,
)

AUTH_TOKEN_PATTERN = '/start ([0-9a-fA-F\-]{36})'


class Commands(Enum):
    START = 'start'
    LIST_TESTS = 'list_tests'
    LEADERBOARD = 'leaderboard'
    # RESUME_TEST = 'resume_test'

    @classmethod
    def list(cls):
        return '/'+'\n/'.join(c.value for c in cls)


@bot.message_handler(regexp=AUTH_TOKEN_PATTERN)
def auth_message(message):
    auth_token = re.match(AUTH_TOKEN_PATTERN, message.text).group(1)
    response = ApiClient(BASE_API_URL).get(path=f'tg_auth/{auth_token}/')
    user_id_map[message.chat.id] = User(**response)
    start_message(message)


@bot.message_handler(regexp='/start$')
@login_required
def start_message(message):
    client_info = user_id_map[message.chat.id]
    bot.send_message(message.chat.id, f'Hi, {client_info.username}! 👋 How are you? 🙃')
    bot.send_message(message.chat.id, f"Please, select one of the available commands:\n{Commands.list()}")


@bot.message_handler(commands=[Commands.LIST_TESTS.value])
@login_required
def list_tests(message):
    tests = TestModelFetcher(message.user).get_list()
    buttons = [
        telebot.types.InlineKeyboardButton(
            text=test.title,
            callback_data=create_callback_data('TEST', test)
        )
        for test in tests
    ]
    keyboard = telebot.types.InlineKeyboardMarkup().row(*buttons)
    bot.send_message(message.chat.id, "Let's select one of the available tests:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: 'TEST' in call.data)
@login_required
def start_new_test(call):
    test = retrieve_callback_data(call.data)
    bot.edit_message_text(
        text=f'Test \'{test.title}\' is chosen!',
        message_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

    TestRunner(call, test.id)\
        .add_callback(TestRunner.NEXT, next)\
        .add_callback(TestRunner.FINISH, finish)\
        .run()


def next(call, test_runner, question_detail):
    choice_buttons = [
        telebot.types.InlineKeyboardButton(
            text=choice.text,
            callback_data=create_callback_data('CHOICE', (choice, test_runner))
        )
        for idx, choice in enumerate(question_detail.choices)
    ]
    keyboard = telebot.types.InlineKeyboardMarkup().row(*choice_buttons)
    bot.send_message(
        chat_id=call.message.chat.id,
        text=f'Question #{test_runner.current_step}/{test_runner.questions_count}: {question_detail.text}',
        reply_markup=keyboard
    )


def finish(call, _, test_result):
    bot.send_message(
        chat_id=call.message.chat.id,
        text=f'{call.user.username}, test is accomplished!\n' +
             'Your result is: ' +
             f'{test_result.num_correct_answers}/{test_result.questions_count}' +
             f'{(test_result.num_correct_answers == test_result.questions_count) and "  Well done! 👍" or ""}'
    )


@bot.callback_query_handler(func=lambda call: 'CHOICE' in call.data)
@login_required
def on_choice_selection(call):
    choice, test_runner = retrieve_callback_data(call.data)

    result_info = '✅' if choice.is_correct else '❌'
    bot.edit_message_text(
        text=f'Answer {test_runner.current_question.text} -> {choice.text}:' + result_info,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

    test_runner.send(choice)


@bot.message_handler(commands=[Commands.LEADERBOARD.value])
@login_required
def show_leaderboard(message):
    users = UserModelFetcher(message.user).get_list()
    leaderboard = '\n'.join(
        f"{user.username:<20} {user.rating}"
        for user in users
    )
    bot.send_message(message.chat.id, f"""LEADERBOARD:
    ```
{leaderboard}
    ```
    """, parse_mode="Markdown")


@bot.message_handler(content_types=['text', 'url'])
def send_text(message):
    bot.send_message(message.chat.id, 'Sorry! Did not get your request: %s' % message.text)
    bot.send_message(message.chat.id, 'Please, try /start command')

