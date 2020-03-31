# Импортируем созданный нами класс Server
from server import Server


vk_api_token = 'bc63767926392be80357a43cbd2e44e6358962c9dbfa72ef804d32d5e90a1e3d623e9bf8bc1ef3a1540b5'
server1 = Server(vk_api_token, 193600928, "server1")

server1.test()
server1.start()