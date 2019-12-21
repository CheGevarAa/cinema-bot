import telebot
import sqlite3
import datetime


conn = sqlite3.connect("cinemabot.db", check_same_thread=False)
cursor = conn.cursor()

bot = telebot.TeleBot('703221413:AAEp4Our51D_KODPh-GHT6E5CLj6hY8wILE')

keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.add('/films', '/cinemas', '/sessions')
keyboard_1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_1.add('/Меню', '/КАРО', '/Синема_ПАРК', '/Алмаз_Синема')
keyboard_2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_2.add('Сеансы на завтра')
dic_films = {i[2] : i[0] for i in cursor.execute("select * from cinema_halls")}
today = (datetime.date.today() + datetime.timedelta(days=0)).strftime('%Y-%m-%d')
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
last_hall_id = [0]
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Приветствую', reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Чем могу помочь?')


@bot.message_handler(commands=['sessions'])
def get_sessions(message):
    bot.send_message(message.chat.id, 'Выберете сеть кинотеатров', reply_markup=keyboard_1)


@bot.message_handler(commands=['Меню'])
def get_back_to_menu(message):
    bot.send_message(message.chat.id, 'Пожалуйста', reply_markup=keyboard)


@bot.message_handler(commands=['КАРО'])
def get_karo(message):
    output = ''
    bot.send_message(message.chat.id, 'Прошу')
    for i in cursor.execute("select * from cinema_halls where brand_id =?", (1,)):
        output = output + '''
                Кинотеатр: {}
                Адрес: {}
                Метро: {}
                '''.format(i[2], i[3], i[4])
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['Синема_ПАРК'])
def get_park(message):
    output = ''
    bot.send_message(message.chat.id, 'Прошу')
    for i in cursor.execute("select * from cinema_halls where brand_id =?", (2,)):
        output = output + '''
                    Кинотеатр: {}
                    Адрес: {}
                    Метро: {}
                    '''.format(i[2], i[3], i[4])
    if len(output) > 4096:
        for x in range(0, len(output), 4096):
            bot.send_message(message.chat.id, output[x:x + 4096])
    else:
        bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['Алмаз_Синема'])
def get_diamond(message):
    output = ''
    bot.send_message(message.chat.id, 'Прошу')
    for i in cursor.execute("select * from cinema_halls where brand_id =?", (3,)):
        output = output + '''
                    Кинотеатр: {}
                    Адрес: {}
                    Метро: {}
                    '''.format(i[2], i[3], i[4])
    bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['films'])
def get_films(message):
    output = ''
    for i in cursor.execute("select * from cinemas").fetchall():
        output = output + '''
        Название: {}
        Длина: {}
        Жанры: {}
        '''.format(i[1], i[2], i[3])
    if len(output) > 4096:
        for x in range(0, len(output), 4096):
            bot.send_message(message.chat.id, output[x:x + 4096])
    else:
        bot.send_message(message.chat.id, output)


@bot.message_handler(commands=['cinemas'])
def get_cinemas(message):
    cinemas = {i[0]: i[1] for i in cursor.execute("select * from brand")}
    output = ''
    for i in cursor.execute("select * from cinema_halls").fetchall():
        output = output + '''
        Сеть: {}
        Кинотеатр: {}
        Адрес: {}
        Метро: {}
        '''.format(cinemas[i[1]], i[2], i[3], i[4])
    if len(output) > 4096:
        for x in range(0, len(output), 4096):
            bot.send_message(message.chat.id, output[x:x + 4096])
    else:
        bot.send_message(message.chat.id, output)


@bot.message_handler(content_types=['text'])
def identify_message(message):
    if message.text in dic_films.keys():
        output = ''
        hall_id = dic_films[message.text]
        last_hall_id.pop()
        last_hall_id.append(hall_id)
        for i in cursor.execute("select * from sessions where hall_id =? and date =?", (hall_id, today)):
            output = output + """
            Название: {}
            Дата: {}
            Время: {}
            Цена: {}
            """.format(i[3], i[4], i[5], i[6])
        if len(output) > 4096:
            for x in range(0, len(output), 4096):
                bot.send_message(message.chat.id, output[x:x + 4096])
        else:
            bot.send_message(message.chat.id, output)
        bot.send_message(message.chat.id, 'ы', reply_markup=keyboard_2)
    elif message.text == 'Сеансы на завтра':
        output = ''
        for i in cursor.execute("select * from sessions where hall_id =? and date =?", (last_hall_id[0], tomorrow)):
            output = output + """
            Название: {}
            Дата: {}
            Время: {}
            Цена: {}
            """.format(i[3], i[4], i[5], i[6])
        if len(output) > 4096:
            for x in range(0, len(output), 4096):
                bot.send_message(message.chat.id, output[x:x + 4096])
        else:
            bot.send_message(message.chat.id, output)
    elif 'русское кино' in message.text.lower() or 'русском кино' in message.text.lower():
        bot.send_sticker(message.chat.id, 'CAADAgADZwAD2kJgEfJf204qqJpmFgQ')


bot.polling(none_stop=True, interval=0)