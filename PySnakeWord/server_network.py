import pygame
import socket, pickle
import select
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

port = 10000
address = "127.0.0.1"

inputs = []
outputs = []
updateClients = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
    socketServer.setblocking(False)
    socketServer.bind((address, port))
    socketServer.listen()
    inputs.append(socketServer)
    while True:
        readable, writable, errs = select.select(inputs, [], [])
        for socks in readable:
            if socks is socketServer:
                try:
                    conn, info = socks.accept()
                    conn.setblocking(False)
                    inputs.append(conn)
                    outputs.append(conn)
                except BlockingIOError:
                    print("Wainting connections")
            else:
                data = socks.recv(4096)
                if data:
                    requireClient = pickle.loads(data)
                    print("Client: ", requireClient["id"], " send data!")
                    if requireClient["id"] == None:
                        newSnake = Snake()
                        idPlayer = manager.addSnakeInGame(newSnake)
                        newSnake.drawSnake(gameSurface)
                        socks.sendall(pickle.dumps({"id": idPlayer}))
                    else:
                        manager.userCommand(requireClient["key"], requireClient["id"])
                        manager.checkSnakeEatFood(requireClient["id"])
                    updateClients = True
                else:
                    inputs.remove(socks)
                    socks.close()

        # Envia para os usuarios a tela do jogo atualizada.
        if updateClients:
            gameSurface.fill((9, 10, 13))
            manager.initGame()
            manager.moveSnakes(gameSurface)
            surfaceToSend = manager.sendSurface()
            r, w, e = select.select([], outputs, [])
            for socketClient in w:
                socketClient.sendall(pickle.dumps(surfaceToSend))
            updateClients = False