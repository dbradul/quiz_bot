import os
import telebot

bot = telebot.TeleBot(os.environ.get('TG_TOKEN'))
