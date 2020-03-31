import vk_api.vk_api
import re

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
        self.vk_api.messages.send(user_id=181178506, message="Привет-привет!", random_id=get_random_id())

    def start(self):
        for event in self.long_poll.listen():   # Слушаем сервер
            # Пришло новое сообщение
            if event.type == VkBotEventType.MESSAGE_NEW:
                if re.findall('откартавь', event.object['message']['text']):
                    res = ''
                    for i in re.findall("откартавь (.*)", event.object['message']['text'])[0]:
                        if i == 'р':
                            res += 'гх'
                        elif i == 'Рэ':
                            res += 'Гх'
                        else:
                            res += i
                    print(res)
                    self.send_message(event.chat_id, res)
                else:
                    self.send_message(event.chat_id, "Ну, я получил твое сообщение, и что?")

    def send_message(self, chat, message):
        self.vk_api.messages.send(chat_id=chat, message=message, random_id=get_random_id())


