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

port = 12000
address = "127.0.0.1"

inputs = []
outputs = []
updateClients = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
    socketServer.setblocking(False)
    socketServer.bind(('', port))
    socketServer.listen()
    inputs.append(socketServer)

    while True:
        readable, writable, errs = select.select(inputs, outputs, [])
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
                    print("Client:", requireClient["id"], "send data!")
                    if requireClient["id"] == None:
                        newSnake = Snake()
                        idPlayer = manager.addSnakeInGame(newSnake)
                        newSnake.drawSnake(gameSurface)
                        socks.sendall(pickle.dumps({"id": idPlayer}))
                    else:
                        if requireClient["key"] != None:
                            manager.userCommand(requireClient["key"], requireClient["id"])
                        else:
                            manager.romoveSnakeOnGame(requireClient["id"])
                            inputs.remove(socks)
                            outputs.remove(socks)
                            writable.remove(socks)
                            socks.close()
                    updateClients = True
                else:
                    inputs.remove(socks)
                    outputs.remove(socks)
                    socks.close()

        # Envia para os usuarios a tela do jogo atualizada.
        if updateClients:
            manager.checksAllSnakeEatFood()
            manager.moveSnakes(gameSurface)
            for sockets in writable:
                sockets.sendall(pickle.dumps({"snakes": manager.snakesToSend(), "foods": manager.foodToSend()}))
            updateClients = False
            #r, w, err = select.select(inputs, [], [], 0.1)