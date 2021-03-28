import json
import telebot
from app.logging import log
from app.bot import bot
from app import api
from app.parsers import create_question_callback_data, parse_question_callback_data, create_test_callback_data, \
    parse_test_callback_data

COMMANDS_LIST_TESTS = 'list_tests'
COMMANDS_LEADERBOARD = 'leaderboard'


@log
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Hi, you sent me /start')
    bot.send_message(message.chat.id, f"""List of available commands:
        /{COMMANDS_LIST_TESTS}
        /continue_test
        /{COMMANDS_LEADERBOARD}
    """)

    bot.send_message(message.chat.id, "Please, select one of commands")


@log
@bot.message_handler(commands=[COMMANDS_LIST_TESTS])
def list_tests(message):
    tests = api.get_tests()
    buttons = [
        telebot.types.InlineKeyboardButton(text=test.get('title'),  callback_data=create_test_callback_data(test))
        for test in tests
    ]
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(*buttons)
    bot.send_message(message.chat.id, "Let's select one of the available tests:", reply_markup=keyboard)


@log
@bot.callback_query_handler(func=lambda call: 'test_id' in call.data)
def start_new_test(call):
    test_id = parse_test_callback_data(call.data)
    test = api.get_test(test_id)
    test_result = api.create_test_result(test_id)
    call.data = {'test_result': test_result}
    bot.edit_message_text(
        text=f'Test \'{test.get("title")}\' is choosen!',
        message_id=call.message.message_id,
        chat_id=call.message.chat.id)
    next_question(call)


# @log
@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('test_result'))
def next_question(call):
    test_result = call.data.get('test_result')
    test_result = api.get_test_result(test_result.get('id'))
    question = api.get_test_question(
        test_result.get('test'),
        test_result.get(api.RESULT_FIELD_CURRENT_ORDER_NUMBER)
    )

    keyboard = telebot.types.InlineKeyboardMarkup()
    test_buttons = [
        telebot.types.InlineKeyboardButton(
            text=choice.get('text'),
            callback_data=create_question_callback_data(choice, test_result)
        )
        for idx, choice in enumerate(question.get('choices'))
    ]
    keyboard.row(*test_buttons)
    info = f'#{test_result.get(api.RESULT_FIELD_CURRENT_ORDER_NUMBER)}/{test_result.get(api.RESULT_FIELD_QUESTIONS_COUNT)}: '\
            f'{question.get("text")}'
    bot.send_message(
        chat_id=call.message.chat.id,
        text=f'Question {info}',
        reply_markup=keyboard
    )


@log
@bot.callback_query_handler(func=lambda call: 'choice_id' in call.data)
def next_question_on_choice_selection(call):
    choice_id, test_result_id = parse_question_callback_data(call.data)
    test_result = api.get_test_result(test_result_id)
    choice = api.get_choice(choice_id)
    question = api.get_test_question(
        test_result.get(api.RESULT_FIELD_TEST),
        test_result.get(api.RESULT_FIELD_CURRENT_ORDER_NUMBER)
    )

    payload = {
        'choice_id': choice_id,
        api.RESULT_FIELD_CURRENT_ORDER_NUMBER: test_result.get(api.RESULT_FIELD_CURRENT_ORDER_NUMBER)
    }

    test_result = api.update_test_result(test_result_id, payload=payload)

    info = f'{"CORRECT 👍" if choice.get("is_correct") else "INCORRECT 😢"}'

    bot.edit_message_text(
        text=f'Answer {question.get("text")}={choice.get("text")} is given ({info})!',
        message_id=call.message.message_id,
        chat_id=call.message.chat.id
    )

    if test_result.get('get_state_display') == api.TEST_STATE_FINISHED:
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Test is accomplished!\n'\
                 'Your result is: '\
                 f'{test_result.get("num_correct_answers")}/{test_result.get(api.RESULT_FIELD_QUESTIONS_COUNT)}'
        )
    else:
        test_result=api.update_test_result(
            test_result_id=test_result_id,
            payload={api.RESULT_FIELD_CURRENT_ORDER_NUMBER: test_result.get(api.RESULT_FIELD_CURRENT_ORDER_NUMBER) + 1}
        )
        call.data = {'test_result': test_result}
        next_question(call)


@log
@bot.message_handler(commands=[COMMANDS_LEADERBOARD])
def show_leaderboard(message):
    users = api.get_users()
    leaderboard = '\n'.join(
        f"{user[api.USER_FIELD_USERNAME]:<20} {user[api.USER_FIELD_RATING]}"
        for user in users
    )
    bot.send_message(message.chat.id, f"""LEADERBOARD:
    ```
{leaderboard}
    ```
    """, parse_mode="Markdown")


@log
@bot.message_handler(content_types=['text', 'url'])
def send_text(message):
    bot.send_message(message.chat.id, 'Sorry! Did not get your request: %s' % message.text)
