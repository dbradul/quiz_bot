from enum import Enum

import telebot

from app.fetchers import TestFetcher, TestResultFetcher, QuestionFetcher, UserFetcher
from app.logging import log
from app.bot import bot
from app.controllers import TestRunner
from app.models import Test, TestResult
from app.utils import (
    retrieve_callback_data,
    create_callback_data,
)

class Commands(Enum):
    START = 'start'
    LIST_TESTS = 'list_tests'
    LEADERBOARD = 'leaderboard'
    # RESUME_TEST = 'resume_test'

    @classmethod
    def list(cls):
        return '/'+'\n/'.join(c.value for c in cls)


@log()
@bot.message_handler(commands=[Commands.START.value])
def start_message(message):
    bot.send_message(message.chat.id, 'Hi, you\'ve sent me /start')
    bot.send_message(message.chat.id, f"""List of available commands:\n{Commands.list()}""")
    bot.send_message(message.chat.id, "Please, select one of commands")


@log()
@bot.message_handler(commands=[Commands.LIST_TESTS.value])
def list_tests(message):
    tests = TestFetcher.get_list()
    buttons = [
        telebot.types.InlineKeyboardButton(
            text=test.title,
            callback_data=create_callback_data('TEST', test)
        )
        for test in tests
    ]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*buttons)
    bot.send_message(message.chat.id, "Let's select one of the available tests:", reply_markup=keyboard)


@log()
@bot.callback_query_handler(func=lambda call: 'TEST' in call.data)
def start_new_test(call):
    test = retrieve_callback_data(call.data)
    test_detail = TestFetcher.get_object(test.id)
    test_result = TestResultFetcher.post_object(parent_id=test.id, data={
        'state': TestResult.State.NEW.value,
        'current_order_number': 1,
    })
    bot.edit_message_text(
        text=f'Test \'{test.title}\' is chosen!',
        message_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

    # test_runner = TestRunner(test_detail)
    next_question(call, test_detail, test_result)
    # next_question(call, test_runner)


@log()
def next_question(call, test, test_result):
    question = test.questions[test_result.current_order_number-1]
    question_detail = QuestionFetcher.get_object(question.id)
    test_buttons = [
        telebot.types.InlineKeyboardButton(
            text=choice.text,
            callback_data=create_callback_data('CHOICE', (choice, test, test_result))
        )
        for idx, choice in enumerate(question_detail.choices)
    ]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*test_buttons)
    bot.send_message(
        chat_id=call.message.chat.id,
        text=f'Question #{test_result.current_order_number}/{test_result.questions_count}: {question.text}',
        reply_markup=keyboard
    )


@log()
@bot.callback_query_handler(func=lambda call: 'CHOICE' in call.data)
def on_choice_selection(call):
    choice, test, test_result = retrieve_callback_data(call.data)
    question = test.questions[test_result.current_order_number-1]

    result_info = '✅' if choice.is_correct else '❌'
    bot.edit_message_text(
        text=f'Answer {question.text} -> {choice.text}:' + result_info,
        message_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

    test_result.num_correct_answers += int(choice.is_correct)
    test_result.num_incorrect_answers += 1 - int(choice.is_correct)

    if test_result.current_order_number == test_result.questions_count:
        test_result = TestResultFetcher.update_object(test_result)
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Test is accomplished!\n'\
                 'Your result is: '\
                 f'{test_result.num_correct_answers}/{test_result.questions_count}'\
                 f'{(test_result.num_correct_answers == test_result.questions_count) and "Well done! 👍" or ""}'
        )
    else:
        test_result.current_order_number += 1
        test_result = TestResultFetcher.update_object(test_result)
        next_question(call, test, test_result)


@log
@bot.message_handler(commands=[Commands.LEADERBOARD.value])
def show_leaderboard(message):
    users = UserFetcher.get_list()
    leaderboard = '\n'.join(
        f"{user.username:<20} {user.rating}"
        for user in users
    )
    bot.send_message(message.chat.id, f"""LEADERBOARD:
    ```
{leaderboard}
    ```
    """, parse_mode="Markdown")


@log()
@bot.message_handler(content_types=['text', 'url'])
def send_text(message):
    bot.send_message(message.chat.id, 'Sorry! Did not get your request: %s' % message.text)
    bot.send_message(message.chat.id, 'Please, try /start command')
