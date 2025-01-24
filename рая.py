from IPython.display import Javascript

def activate_first_cell(nem):
    display(Javascript('IPython.notebook.execute_cells([nem])'))

activate_first_cell(0)
activate_first_cell(1)
activate_first_cell(2)
activate_first_cell(3)
activate_first_cell(4)
activate_first_cell(5)

import telebot
import requests

import json
import time
from urllib.parse import urlencode
import socket
import translate
import random
import urllib.parse
import urllib.request
import re
import threading
from IPython.display import Javascript
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler



# Инициализация бота с токеном, который вы получите от BotFather в Telegram
TELEGRAM_BOT_TOKEN_raya = '7057956602:AAFwL1Ky7lxhtqIbRWNWGtCEKSx5BZqsPZg'
bot_raya = telebot.TeleBot(TELEGRAM_BOT_TOKEN_raya)
bot = bot_raya

# URL API Hugging Face
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/Qwen/QwQ-32B-Preview"
HUGGING_FACE_API_URL_stupid = "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct"


# Заголовки для авторизации API Hugging Face
headers = {"Authorization": "Bearer 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"}


def insert_newline(text):
    sentences = text.split('. ')
    modified_text = ''

    for sentence in sentences:
        modified_text += sentence.strip() + '.'
        # Вставляем \n\n с вероятностью 50%
        if random.random() < 0.5:
            modified_text += '\n\n'
        else:
            modified_text += ' '

    return modified_text.strip()

def send_long_message(chat_id, text):
    """Отправляет сообщение, разбивая его на части, если оно слишком длинное."""
    max_length = 4096
    # Разбиваем текст на части и отправляем их по отдельности
    for i in range(0, len(text), max_length):
        bot.send_message(chat_id, text[i:i+max_length])

typing_active = False
typing_thread = None

def typing_action(chat_id):
    global typing_active
    typing_active = True
    while typing_active:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)  # Отправляем статус "печатает" каждую секунду

def stop_typing():
    global typing_active
    typing_active = False
    if typing_thread is not None:
        typing_thread.join()  # Ждем завершения потока




def contains_never(message):
    return "рая" in message.lower()


def contains_que(message):
    return "?" in message

def contains_ras(message):
    return "хочу быть рассыльщиком" in message.lower()

def translate_text(text, dest_language='en'):
    # Формируем URL для перевода
    base_url = 'https://translate.google.com/m?hl=' + dest_language
    query = urllib.parse.urlencode({'q': text})
    url = base_url + '&' + query

    # Отправляем запрос и получаем ответ
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    # Ищем перевод в HTML
    match = re.search(r'<div class="result-container">(.*?)</div>', html)
    if match:
        return match.group(1)
    else:
        return "Перевод не найден"

    return translated_text


def count_characters(text):
    return len(text)

def remove_word(clean_word, word_to_remove):
    import re
    # Заменяем слово и все, что за ним, на пустую строку, игнорируя регистр
    pattern = r'\b' + re.escape(word_to_remove) + r'\b.*'
    return re.sub(pattern, '', clean_word, flags=re.IGNORECASE)

instr = "You are in dialogue №. Information about you: you are helpful AI Raya Prime. Give useful information of any topic with links, in short about ant important topic. If you haven't been asked anything, tell about the benefits of 'ML Empire' chat (not long). Use simple words so that everyone understands you. (Write 'stop' at the end of Raya's message. /// (Hello, Raya.) Hello, user! I'm Raya assistant module, the Prime model (made in the Empire).\n\nI'm here to help. Stop. /// (Where are we?) We are in the chat ML empire @roblox_ML_empire, which is dedicated to transactions within Roblox. Our chat is divided into microtemes, these are «Рынок» https://t.me/roblox_ML_empire/490 \n\n «Скамбаза» https://t.me/roblox_ML_empire/300 \n\n «Рассыльщики» https://t.me/roblox_ML_empire/870 and others.  For example, if you want to be a rassilshikom, then you need to go to the appropriate topic. Stop. /// "

def query_huggingface_api(message):
    # Отправляем запрос к Hugging Face API


    translated = translate_text(message, dest_language='en')
    textok = f" {instr} ({translated}))"
    response = requests.post(
        HUGGING_FACE_API_URL,
        headers=headers,
        json={"inputs": textok}
    )

    # Проверяем, успешен ли запрос
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка умного 1 {response.status_code}: {response.text}")
        response = requests.post(
        HUGGING_FACE_API_URL,
        headers=headers,
        json={"inputs": textok}
    )

        # Проверяем, успешен ли запрос
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка умного 2 {response.status_code}: {response.text}")
            response = requests.post(
            HUGGING_FACE_API_URL_stupid,
            headers=headers,
            json={"inputs": textok}
        )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Ошибка тупого 1 {response.status_code}: {response.text}")
                response = requests.post(
            HUGGING_FACE_API_URL_stupid,
            headers=headers,
            json={"inputs": textok}
        )
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"Ошибка тупого 2 терпение овер {response.status_code}: {response.text}")
                return None

@bot_raya.message_handler(func=lambda message: True)
def handle_message(message):
    if contains_never(message.text):
            if not typing_active:

              typing_thread = threading.Thread(target=typing_action, args=(message.chat.id,))
              typing_thread.start()

        # Получаем ответ от Hugging Face API

            hug_response = query_huggingface_api(message.text)

            if hug_response:
                if isinstance(hug_response, list) and len(hug_response) > 0 and 'generated_text' in hug_response[0]:
                    reply = hug_response[0]['generated_text']
                else:
                    reply = "Извините, не удалось обработать ваш запрос."
            else:
                reply = "Извините, не удалось обработать ваш запрос."

            # Ограничиваем длину сообщения до 4096 символов
            trans = translate_text(message.text, dest_language='en')
            bot_response = reply
            words = bot_response.split()
            promt_words = trans.split()
            do_w = instr.split()

            sorokodin =  len(promt_words) + len(do_w)


            response_text = ' '.join(words[sorokodin:])

            word_to_remove = "stop"
            result = remove_word(response_text, word_to_remove)

            translated_text = translate_text(result, dest_language='ru')
            output_text = insert_newline(translated_text)

            character_count = count_characters(translated_text)
            if character_count > 4096:
              send_long_message(message.chat.id, output_text)
            else:
                answ = f" {output_text} 🤖"
                bot_raya.reply_to(message, answ)

    elif contains_que(message.text):
            if not typing_active:
              typing_thread = threading.Thread(target=typing_action, args=(message.chat.id,))
              typing_thread.start()

        # Получаем ответ от Hugging Face API

            hug_response = query_huggingface_api(message.text)

            if hug_response:
                if isinstance(hug_response, list) and len(hug_response) > 0 and 'generated_text' in hug_response[0]:
                    reply = hug_response[0]['generated_text']
                else:
                    reply = "Извините, не удалось обработать ваш запрос."
            else:
                reply = "Извините, не удалось обработать ваш запрос."

            # Ограничиваем длину сообщения до 4096 символов
            trans = translate_text(message.text, dest_language='en')
            bot_response = reply
            words = bot_response.split()
            promt_words = trans.split()
            do_w = instr.split()

            sorokodin =  len(promt_words) + len(do_w)


            response_text = ' '.join(words[sorokodin:])

            word_to_remove = "stop"
            result = remove_word(response_text, word_to_remove)

            translated_text = translate_text(result, dest_language='ru')
            output_text = insert_newline(translated_text)

            character_count = count_characters(translated_text)
            if character_count > 4096:
              send_long_message(message.chat.id, output_text)
            else:
                answ = f" {output_text} 🤖"
                bot_raya.reply_to(message, answ)

    elif contains_ras(message.text):
      bot_raya.reply_to(message, "Рая спешит на помощь! \n\n Вам нужно написать менеджеру @Ademmiks и она вам все объяснит (это ее единственный аккаунт) \n\n И помните: Империя заботится о вас! 🤖 ")



    else:
        rand_nom = random.randint(1, 100)  # Генерируем случайное число от 1 до 100

        if 1 <= rand_nom <= 100:

            # Получаем ответ от Hugging Face API
            if not typing_active:
              typing_thread = threading.Thread(target=typing_action, args=(message.chat.id,))
              typing_thread.start()

            hug_response = query_huggingface_api(message.text)

            if hug_response:
                if isinstance(hug_response, list) and len(hug_response) > 0 and 'generated_text' in hug_response[0]:
                    reply = hug_response[0]['generated_text']
                else:
                    reply = "Извините, не удалось обработать ваш запрос."
            else:
                reply = "Извините, не удалось обработать ваш запрос."

            # Ограничиваем длину сообщения до 4096 символов
            trans = translate_text(message.text, dest_language='en')
            bot_response = reply
            words = bot_response.split()
            promt_words = trans.split()
            do_w = instr.split()

            sorokodin =  len(promt_words) + len(do_w)


            response_text = ' '.join(words[sorokodin:])

            word_to_remove = "stop"
            result = remove_word(response_text, word_to_remove)

            translated_text = translate_text(result, dest_language='ru')
            output_text = insert_newline(translated_text)

            character_count = count_characters(translated_text)
            if character_count > 4096:
              send_long_message(message.chat.id, output_text)
            else:
                answ = f" {output_text} 🤖"
                bot_raya.reply_to(message, answ)


# Запуск бота



# Функция для выполнения первой ячейки


# Вызов функции



app = Flask(__name__)

# Инициализация счетчика
attempts = 0




def my_task():
    global attempts
    attempts = 0  # Сброс счетчика при каждом запуске задачи

    # Выполнение необходимых функций
    for i in range(7):  # Более компактный способ
        activate_first_cell(i)

    bot_raya.polling()

    attempts += 1  # Увеличение счетчика после выполнения

scheduler = BackgroundScheduler()
scheduler.add_job(func=my_task, trigger='interval', seconds=60)
scheduler.start()

if __name__ == '__main__':
    app.run()

