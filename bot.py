import config
import telebot
from telebot import types  # кнопки
from string import Template

bot = telebot.TeleBot(config.TOKEN)

user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'phone', 'city',
                'region', 'rooms', 'class']

        for key in keys:
            self.key = None


# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/rent')
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Здравствуйте "
                     + message.from_user.first_name
                     + ", я бот, чтобы вы хотели узнать?", reply_markup=markup)


# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Мы предоставляем услуги"
                     + " по аренде квартир")


# /rent
@bot.message_handler(commands=["rent"])
def user_rent(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Астана')
    itembtn2 = types.KeyboardButton('Караганды')
    #itembtn3 = types.KeyboardButton('Алматы')
    #itembtn4 = types.KeyboardButton('Шымкент')
    #itembtn5 = types.KeyboardButton('Актау')
    #itembtn6 = types.KeyboardButton('Атырау')
    #markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, 'Ваш город?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    chat_id = message.chat.id
    print(chat_id)
    # user = user_dict[chat_id]
    # user.city = message.text
    user_dict[chat_id] = User(message.text)

    if message.text == 'Астана':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Есильский')
        itembtn2 = types.KeyboardButton('Алматинский')
        itembtn3 = types.KeyboardButton('Сарыаркинский')
        itembtn4 = types.KeyboardButton('Байконурский')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    if message.text == 'Караганды':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Октябрьский')
        itembtn2 = types.KeyboardButton('Казыбекбийский')
        markup.add(itembtn1, itembtn2)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton('Район 1')
        itembtn2 = types.KeyboardButton('Район 2')
        itembtn3 = types.KeyboardButton('Район 3')
        itembtn4 = types.KeyboardButton('Район 4')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    msg = bot.send_message(message.chat.id, 'Ваш район?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_regoin_step)


def process_regoin_step(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.region = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('1-комн')
    itembtn2 = types.KeyboardButton('2-комн')
    itembtn3 = types.KeyboardButton('3-комн')
    itembtn4 = types.KeyboardButton('4-комн')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    msg = bot.send_message(message.chat.id, 'Какая квартира?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_rooms_step)


def process_rooms_step(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.rooms = message.text

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Стандарт')
    itembtn2 = types.KeyboardButton('Элит')
    markup.add(itembtn1, itembtn2)

    msg = bot.send_message(message.chat.id, 'Какой класс квартиры?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_class_step)


def process_class_step(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.classs = message.text

    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(chat_id, 'Фамилия Имя Отчество', reply_markup=markup)
    bot.register_next_step_handler(msg, process_fullname_step)


def process_fullname_step(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.fullname = message.text

    msg = bot.send_message(chat_id, 'Ваш номер телефона')
    bot.register_next_step_handler(msg, process_phone_step)


def process_phone_step(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    user.phone = message.text

    #    msg = bot.send_message(chat_id, 'Ваша заявка принята!')
    #    bot.register_next_step_handler(msg, getRegData)
    # ваша заявка "Имя пользователя"
    bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")

    # отправить в группу
    bot.send_message(config.chat_id1, getRegData(user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")


# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template(
        '$title *$name* \n Город: *$userCity* \n Район: *$userRegion* \n Количество комнат: *$userRooms* \n Класс квартиры: *$userClass* \n ФИО: *$fullname* \n Телефон: *$phone*')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'userRegion': user.region,
        'userRooms': user.rooms,
        'userClass': user.classs,
        'fullname': user.fullname,
        'phone': user.phone
    })


# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    #bot.send_message(message.chat.id, 'О нас - /about\nЗаявка на аренду квартиры - /rent\nПомощь - /help')
    a = 1


# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
