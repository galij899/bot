import vk_api.vk_api
import json
import re
import random
import time

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class Server:

    def __init__(self, api_token, group_id, server_name: str="Empty"):

        # giving name to server
        self.server_name = server_name

        # for Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # for Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id, wait=20)

        # for vk_api methods
        self.vk_api = self.vk.get_api()

        self.test()

    def test(self):
        self.vk_api.messages.send(user_id=181178506, message="Бот запущен" + " " + time.ctime(), random_id=get_random_id())

    def error_send(self, error):
        self.vk_api.messages.send(user_id=181178506, message=' '.join(["Ошибка", error, "в", time.ctime()]), random_id=get_random_id())

    def get_user_name(self, user_id):
        """ Получаем имя пользователя"""
        return self.vk_api.users.get(user_id=user_id)[0]['first_name']

    def get_user_link(self, user_id):
        load = self.vk_api.users.get(user_id=user_id) # [id213000146|@jenkeyx]
        return "[id" + str(user_id) + "|" + load[0]['first_name'] + " " + load[0]['last_name'] + "]"

    def start(self):

        for event in self.long_poll.listen():   # listening to the server
            # got new message event
            print(event)
            print(event.chat_id)
            if event.type == VkBotEventType.MESSAGE_NEW: #or event.type == VkBotEventType.MESSAGE_REPLY:
                #print(event.object)
                if re.findall('откартавь', event.object['message']['text']):
                    res = ''
                    message = re.findall("откартавь (.*)", event.object['message']['text'])
                    if message:
                        for i in message[0]:
                            if i == 'р' or i == 'p':
                                res += 'гх'
                            elif i == 'Рэ' or i == 'P':
                                res += 'Гх'
                            else:
                                res += i
                        print(res)
                        self.send_message(event.chat_id, res)
                    else:
                        self.send_message(event.chat_id, 'Нечего тут откартавить')

                elif re.findall('волк', event.object['message']['text']):
                    with open("wolfs.json", "r") as read_file:
                        data = json.load(read_file)
                    i = random.randrange(0, len(data['quotes']), 1)
                    self.send_message(event.chat_id, data['quotes'][i])

                elif re.findall('Кто тут батя?', event.object['message']['text']):
                    self.send_message(event.chat_id, "Олег конечно")

                elif re.findall('Войти в игру', event.object['message']['text']):
                    self.add_player(event.object['message']['from_id'], event.chat_id)

                elif re.findall('Рулеточка', event.object['message']['text']):
                    self.start_game(event.chat_id)

                elif re.findall('Статистика', event.object['message']['text']):
                    # self.send_message(event.chat_id, "В разработке")
                    self.stats(event.chat_id)

                elif re.findall('Помощь', event.object['message']['text']):
                    self.game_help(event.chat_id)

                elif re.findall('тест', event.object['message']['text']):
                    self.testing_users(event.chat_id, event.object['message']['from_id'])

                elif re.findall('кинь ошибку', event.object['message']['text']):
                    self.error()

                #else:
                #    self.send_message(event.chat_id, "Ну, я получил твое сообщение, и что?")

    def send_message(self, chat, message):
        self.vk_api.messages.send(chat_id=chat, message=message, random_id=get_random_id())

    def add_chat(self, chat_id):
        with open("roulette.json", "r") as file:
            load = json.load(file)
            if str(chat_id) not in list(load["chats"].keys()):
                load["chats"][str(chat_id)] = {"players":{}}
        with open('roulette.json', 'w') as file:
            json.dump(load, file)

    def add_player(self, user_id, chat_id):
        self.add_chat(chat_id)
        if str(user_id) in self.get_chat_stats(chat_id).keys():
            self.send_message(chat_id, 'Уже в списках')
        else:
            with open("roulette.json", "r") as file:
                load = json.load(file)
            load["chats"][str(chat_id)]["players"][str(user_id)] = 0
            with open('roulette.json', 'w') as file:
                json.dump(load, file)
            self.send_message(chat_id, 'Добавил в приказ на отчисление')

    def start_game(self, chat_id):
        if self.get_chat_stats(chat_id).keys():
            winner = random.choice(list(self.get_chat_stats(chat_id).keys()))
            self.send_message(chat_id, self.get_user_link(winner) + ', ты умер')
            self.death_count(winner, chat_id)
        else:
            self.send_message(chat_id, 'Так никто ж не участвует')

    def game_help(self, chat_id):
        self.send_message(chat_id, 'как работает бот рулет очка:\n 1. напишите "Войти в игру" для участия\n 2. напишите "Рулеточка" для начала игры\n 3. напишите "Статистика" для понятно чего')

    def stats(self, chat_id):
        m = "Статистика смертей:\n\n" + "\n".join([self.get_user_link(key) + " - " + str(self.get_chat_stats(chat_id)[key]) for key in self.get_chat_stats(chat_id).keys()])
        self.send_message(chat_id, m)

    def death_count(self, user_id, chat_id):
        with open("roulette.json", "r") as file:
            load = json.load(file)
        load["chats"][str(chat_id)]["players"][str(user_id)] = load["chats"][str(chat_id)]["players"][str(user_id)] + 1
        with open('roulette.json', 'w') as file:
            json.dump(load, file)

    def get_chat_stats(self, chat_id):
        with open("roulette.json", "r") as file:
            load = json.load(file)
        return load["chats"][str(chat_id)]["players"]

    def testing_users(self, chat_id, user_id):
        self.send_message(chat_id, self.vk_api.users.get(user_id=user_id))

    def error(self):
        1 / 0

    def error_log(self, error):
        with open("log.csv", "a") as file:
            file.write(','.join([str(time.time()), error]) + "\n")
