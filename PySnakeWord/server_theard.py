import pygame
import socket, pickle
import select
import threading
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
clientsThreads = []
updateClients = False
data = []
newDataFromClients = False
requireClient = {}
newClient = 0
mutex = threading.Lock()

def clientInput(clientSocket):
    global data
    global requireClient
    global newClient
    global newDataFromClients
    global outputs
    clientConnect = True
    while clientConnect:
        readable, writable, errs = select.select([clientSocket], [], [])
        print("after select func")
        for socks in readable:
            data = socks.recv(4096)
            # newClient = socks
        if data:
            requireClient_local = pickle.loads(data)

            mutex.acquire()
            requireClient = {"socketClient": clientSocket, "clientData": requireClient_local}
            newDataFromClients = True
            mutex.release()
        else:
            clientConnect = False
            outputs.remove(clientSocket)
            clientSocket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
    socketServer.setblocking(False)
    socketServer.bind(('', port))
    socketServer.listen()
    inputs.append(socketServer)

    while True:
        newClient, writable, erros = select.select([socketServer], outputs, [])
        #print("after select")
        for socket in newClient:
            try:
                conn, info = socket.accept()
                conn.setblocking(False)
                outputs.append(conn)
                t = threading.Thread(target=clientInput, args=([conn]))
                t.start()
            except BlockingIOError:
                print("no connections!")

        if newDataFromClients:
            if data:
                # requireClient = pickle.loads(data)
                print("Client:", requireClient["clientData"]["id"], "send data!")
                if requireClient["clientData"]["id"] == None:
                    newSnake = Snake()
                    idPlayer = manager.addSnakeInGame(newSnake)
                    newSnake.drawSnake(gameSurface)
                    requireClient["socketClient"].sendall(pickle.dumps({"id": idPlayer}))
                else:
                    if requireClient["clientData"]["key"] != None:
                        manager.userCommand(requireClient["clientData"]["key"], requireClient["clientData"]["id"])
                        print("comando do cliente")
                    else:
                        manager.romoveSnakeOnGame(requireClient["clientData"]["id"])
                        outputs.remove(requireClient["socketClient"])
                        writable.remove(requireClient["socketClient"])
                        requireClient["socketClient"].close()
                updateClients = True
                newDataFromClients = False
            # else:
            #     outputs.remove(requireClient["socketClient"])
            #     requireClient["socketClient"].close()

        # Envia para os usuarios a tela do jogo atualizada.
        if updateClients:
            manager.checksAllSnakeEatFood()
            manager.moveSnakes(gameSurface)
            for sockets in writable:
                sockets.sendall(pickle.dumps({"snakes": manager.snakesToSend(), "foods": manager.foodToSend()}))
            updateClients = False
            #r, w, err = select.select(inputs, [], [], 0.1)