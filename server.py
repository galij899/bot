import vk_api.vk_api
import json
import re
import random

from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType


class Server:

    def __init__(self, api_token, group_id, server_name: str="Empty"):

        # Даем серверу имя
        self.server_name = server_name

        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использоания Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id, wait=20)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def test(self):
        self.vk_api.messages.send(user_id=181178506, message="Бот запущен", random_id=get_random_id())

    def start(self):
        for event in self.long_poll.listen():   # Слушаем сервер
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                # print([event.object['message']['text']])

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

                else:
                    self.send_message(event.chat_id, "Ну, я получил твое сообщение, и что?")

    def send_message(self, chat, message):
        self.vk_api.messages.send(chat_id=chat, message=message, random_id=get_random_id())


