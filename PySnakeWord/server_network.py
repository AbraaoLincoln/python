import pygame
import socket, pickle
import time

from snake.model.Snake import Snake
from snake.model.GameBoard import GameBoard
from snake.controle.GameManeger import GameManeger

try:
    pygame.init()
except:
    print("Não foi possivel iniciar o pygame")

gameSurface = pygame.Surface((GameBoard.width, GameBoard.height))
manager = GameManeger(gameSurface)
gameSurface.fill((9, 10, 13))

port = 12000
address = "127.0.0.1"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setblocking(False)
    sock.bind((address, port))
    sock.listen()

    while True:
        try:
            conn, info = sock.accept()
            while True:
                data = conn.recv(4096)
                if data:
                    requireClient = pickle.loads(data)
                    print(requireClient["id"])
                    if requireClient["id"] == None:
                        newSnake = Snake()
                        idPlayer = manager.addSnakeInGame(newSnake)
                        newSnake.drawSnake(gameSurface)
                        surfaceToSend = manager.sendSruface()
                        conn.sendall(pickle.dumps({"id": idPlayer, "gameScreen": surfaceToSend}))
                    else:
                        manager.userCommand(requireClient["key"], requireClient["id"])
                        gameSurface.fill((9, 10, 13))
                        manager.moveSnakes(gameSurface)
                        surfaceToSend = manager.sendSruface()
                        conn.sendall(pickle.dumps(surfaceToSend))

        except BlockingIOError:
            print("Waiting for connections")
            time.sleep(1)