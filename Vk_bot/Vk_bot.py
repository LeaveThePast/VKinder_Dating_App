import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
from configparser import ConfigParser
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def open_a_token(file_name):
    """Открытие токана для бота"""
    cofing = ConfigParser()
    cofing.read(file_name)
    group_token = cofing["Vk_info"]["group_token"]
    return group_token


class VkBot:
    def __init__(self, open_a_token):
        """Подключение к боту"""
        self.vk_session = vk_api.VkApi(token=open_a_token)
        self.vk_api = self.vk_session.get_api()
        self.long_pool = VkLongPoll(self.vk_session)

    def write_msg(self, user_id, message, keyboard=None, attachment=None):
        """Сообщение от бота: кому, сообщение, id собщения, кнопки, картинки"""
        post = {
            "user_id": user_id,
            "message": message,
            "random_id": randrange(10**7),
        }
        if attachment != None:
            post["attachment"] = attachment
        else:
            post = post
        if keyboard != None:
            post["keyboard"] = keyboard.get_keyboard()
        else:
            post = post
        self.vk_session.method("messages.send", post)

    def but_col(self):
        """Список цветов"""
        buttons_colors = [
            VkKeyboardColor.POSITIVE,
            VkKeyboardColor.NEGATIVE,
            VkKeyboardColor.PRIMARY,
            VkKeyboardColor.SECONDARY,
        ]
        return buttons_colors

    def set_key_parameters(self, buttons, but_col):
        """Задаём цвет, количество кнопок в ответе бота"""
        keyboard = VkKeyboard(inline=True)
        if not isinstance(buttons, list) and not isinstance(but_col, list):
            buttons = [buttons]
            but_col = [but_col]
        count = 0
        for bnt, bnt_colors in zip(buttons, but_col):
            if count == 2:
                keyboard.add_line()
            keyboard.add_button(bnt, bnt_colors)
            count += 1
        # keyboard.add_line()
        # keyboard.add_button("Отмена", self.but_col()[1])
        return keyboard

    def get_message(self):
        """Собщения боту от пользователя"""
        for event in self.long_pool.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                message = event.text.lower()
                user_id = event.user_id
                return message, user_id

    def command_list_output(self):
        response = "Добро пожаловать в бот Vkinder."
        return response


def greetings_bot():
    buttons = [
        "Вывести список изюранных",
        "Вывести черный список",
        "Вывести список понравившихся",
        "Начать поиск",
        "Завершить работу с ботом",
    ]
    bot_col = vk_session.but_col()
    keyboard = vk_session.set_key_parameters(
        buttons, [bot_col[2], bot_col[2], bot_col[2], bot_col[0], bot_col[1]]
    )
    return keyboard


if __name__ == "__main__":
    while True:
        vk_session = VkBot(open_a_token("confing.ini"))
        message, user_id = vk_session.get_message()
        if message.lower() == "привет":
            keyboard = greetings_bot()
            vk_session.write_msg(user_id, vk_session.command_list_output(), keyboard)
            message, user_id = vk_session.get_message()
            if message == "Вывести список изюранных":
                if favorites_list == []:
                    msg = "Список избранных пуст"
                    bot_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters("Назад", bot_col[1])
                    vk_session.write_msg(user_id, msg, keyboard)
                else:
                    msg = "Список избранных"
                    # Функция вывода избранных
                    get_favorites()  # # Дальше управление с Бот и БД, удалить, перенести и т.д
            elif message == "Вывести список понравившихся":
                if like_list == []:
                    msg = "Список избранных пуст"
                    bot_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters("Назад", bot_col[1])
                else:
                    msg = "Список понравившихся"
                    get_liked()  # # Дальше управление с Бот и БД, удалить, перенести и т.д
            elif message == "Вывести черный список":
                if black_list == []:
                    msg = "Черный список пуст"
                    bot_col = vk_session.but_col()
                    keyboard = vk_session.set_key_parameters("Назад", bot_col[1])
                    vk_session.write_msg(user_id, msg, keyboard)
                else:
                    msg = "Список понравившихся"
                    get_black_list()  # Дальше управление с Бот и БД, удалить, перенести и т.д
            elif message == "Завершить работу с ботом":
                msg = "До свидания"
                break
            elif message == "Назад":
                keyboard = greetings_bot()
                vk_session.write_msg(
                    user_id, vk_session.command_list_output(), keyboard
                )
            elif message == "Начать поиск":
                msg = "Выберите пол особи"
                buttons = ["Особь женского пола", "Особь мужского пола"]
                keyboard = vk_session.set_key_parameters(
                    buttons, [bot_col[0], bot_col[2]]
                )
                vk_session.write_msg(user_id, msg, keyboard)
                message, user_id = vk_session.get_message()
                if message == "Особь женского пола":
                    msg = "Выбирете возсрат особи"
                    buttons = ["18-25", "26-35", "36-45", "46-55", "56+", "Назад"]
                    keyboard = vk_session.set_key_parameters(
                        buttons,
                        [
                            bot_col[3],
                            bot_col[3],
                            bot_col[3],
                            bot_col[3],
                            bot_col[3],
                            bot_col[1],
                        ],
                    )
                    vk_session.write_msg(user_id, msg, keyboard)
                    message, user_id = vk_session.get_message()
                    if message in ["18-25", "26-35", "36-45", "46-55", "56+"]:
                        msg = "Выбирете "
                        buttons = ["18-25", "26-35", "36-45", "46-55", "56+", "Назад"]
        elif message == "2":
            vk_session.write_msg(user_id, "See you later", keyboard)
            break
