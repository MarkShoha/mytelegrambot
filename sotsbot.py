import random
# Подключаем модуль для Телеграма
import telebot
from paho.mqtt.client import Client

bot = telebot.TeleBot('5146873101:AAFJ79AWuv2Zf20pfi9eKzN-AgNGEyWHNK0')
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
global g
g=random.randint(0,2)
def receive_message(device, userdata, message):
    global mqtt_message
    mqtt_message = message.payload.decode()
    # Если юзер прислал 1, выдаем ему случайный факт
    if mqtt_message == '1' :
        keyboard = types.InlineKeyboardMarkup()

        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_oven = types.InlineKeyboardButton(text='задача', callback_data='zodiac')
        # И добавляем кнопку на экран
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='тренировка', callback_data='zodiac1')
        keyboard.add(key_telec)
        bot.send_sticker(id,
                         'CAACAgIAAxkBAAIBL2IU4Kn-U_GGxxYyRF6ir1tTJv_AAAIVAAPANk8TzVamO2GeZOcjBA')
        bot.send_message(id, text='Ты весёлый.\n Выбери своё развлечение', reply_markup=keyboard)


    # Если юзер прислал 2, выдаем умную мысль
    elif mqtt_message == '0':
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_oven = types.InlineKeyboardButton(text='анекдот', callback_data='zodiac2')
        # И добавляем кнопку на экран
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='фильм', callback_data='zodiac12')
        keyboard.add(key_telec)
        bot.send_sticker(id,
                         'CAACAgIAAxkBAAIBMWIU4LGIqTndlBUKkaRKkGZw8y8ZAAIgAAPANk8T9A8ruj5f9M8jBA')
        bot.send_message(id, text='Ты грустный.\nВыбери своё развлечение', reply_markup=keyboard)

    # Если юзер прислал 2, выдаем умную мысль
    # Отсылаем юзеру сообщение в его чат


# Указываем токен
@bot.message_handler(commands=["start"])
def start(m, res=False):
        # Добавляем две кнопки
        global id,q_f
        q_f = ['все', 'лёд', 'медуза']
        id = m.chat.id
        bot.send_sticker(m.chat.id,
                         'CAACAgIAAxkBAAIBLWIU4I-OAjYuRdF3Z-7h6uOX72FkAAIYAAPANk8T1vonv5xqGPgjBA')
        bot.send_message(m.chat.id, 'здравствуйте я sotsbot и я узнаю ваше настроение и помогу вам развится и повесилится')


# Получение сообщений от юзера
# @bot.message_handler(content_types=["text"])
# def handle_text(message):


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    first = ['Сколько месяцев в году имеют 28 дней?',  'Что в огне не горит и в воде не тонет?',
             'Кого австралийцы называют морской осой?']

    first1 = [  'отжмись 20 раз', 'присядь 40 раз', 'пробеги километр','планка 40 секунд']
    first2 = [ 'Ещё в годы правления императрицы Елизаветы был издан указ, запрещающий взяточничество государственных чиновников. Скажите, а когда этот указ вступит в силу?  ','— Алло! Это телефон помощи алкоголикам? — Да. — Скажите, а как делать мохито? ','Если ребенок не хочет есть мясо, чем его заменить? — Собакой. Собака всегда хочет есть мясо.','Есть французская пословица: всю первую половину жизни мы ждём вторую, а всю вторую — вспоминаем первую...']
    first12 = ['бегущий в лабиринте', 'люси', 'человек паук нет пути домой','конек горбунок']
    if call.data == "zodiac2":
        # Формируем гороскоп
        msg = random.choice(first2)
        # Отправляем текст в Телеграм
        print(msg)
        bot.send_message(call.message.chat.id,'Вы выбрали анекдот.\nАндекдот: '+ msg)
    if call.data == "zodiac12":
        # Формируем гороскоп
        msg = random.choice(first12)
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id,'вы выбрали фильмы: \nФильм: ' +msg)
    if call.data == "zodiac":
        # Формируем гороскоп

        msg = first[g]

        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id,'вы выбрали задачу. \nЗадача:'+ msg)
    if call.data == "zodiac1":
        # Формируем гороскоп
        msg = random.choice(first1)
        # Отправляем текст в Телеграм
        bot.send_message(call.message.chat.id,'вы выбрали тренировку. \nТренировка:' +msg)
# Запускаем бота


@bot.message_handler(content_types=['text'])
def text(message):

    q = q_f[g]
    print(id,q)
    if message.text == q:
        bot.send_message(id, 'правильно')
    else:
        bot.send_message(id, 'ты бот а я бог')
    print(message.chat.id, message.text)

    device.publish("client_sasha/social_bot", message.text)

device = Client()
device.username_pw_set("client_sasha", "dsr4mn")
device.connect("mqtt.pi40.ru", 1883)
device.subscribe("client_sasha/social_bot")
device.on_message = receive_message
device.loop_start()
mqtt_message = ''
id = ''

bot.polling(none_stop=True)