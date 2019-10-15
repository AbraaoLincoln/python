import pygame
import socket, pickle
import select
import threading
import time
import signal
import os

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

port = 15000
address = "127.0.0.1"

mutex = threading.Lock()
updateClients = False
data = []
newDataFromClients = False
requireClient = {}
activeThreads = 0
threadsThatAlreadyUpdateClients = 0

doingLogicOfGame = 0
doingIO = 0

def interuptionHandler(sig_number, sig_stack):
    print("Servidor Encerrado")
    print("Tempo gasto com o processamento da logica do jogo:", doingLogicOfGame, "segundos.")
    print("Tempo gasto com o processamento da I/O do jogo:", doingIO, "segundos.")
    os.kill(os.getpid(), signal.SIGKILL)
    thread_food.join()

signal.signal(signal.SIGINT, interuptionHandler)

def clientInput(clientSocket):
    global data
    global requireClient
    global newDataFromClients
    global activeThreads
    global threadsThatAlreadyUpdateClients
    global doingIO
    clientConnect = True

    while clientConnect:
        try:
            star_time = time.time()
            data = clientSocket.recv(4096)
            doingIO += (time.time() - star_time)
            if data:
                requireClient_local = pickle.loads(data)
                #Verifica se o cliente fechou a tela do jogo
                if requireClient_local["id"] != None and requireClient_local["key"] == None:
                    clientConnect = False
                mutex.acquire()
                requireClient = {"socketClient": clientSocket, "clientData": requireClient_local}
                newDataFromClients = True
                mutex.release()
            else:
                print("No data from client")
                clientConnect = False
        except BlockingIOError:
            if clientConnect and updateClients:
                star_time = time.time()
                clientSocket.sendall(pickle.dumps(
                    {"snakes": manager.snakesToSend(), "foods": manager.foodToSend(), "snakeStillInGame": True}))
                doingIO += (time.time() - star_time)
                threadsThatAlreadyUpdateClients += 1
                time.sleep(0.1)
    activeThreads -= 1
    print("Thread encerrada!")

def gen_food():
    global activeThreads
    global doingLogicOfGame
    while True:
        if activeThreads > 0:
            time.sleep(5)
            star_time = time.time()
            manager.addFoodInGame()
            doingLogicOfGame += (time.time() - star_time)

thread_food = threading.Thread(target=gen_food, args=())
thread_food.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketServer:
    socketServer.setblocking(False)
    socketServer.bind(('', port))
    socketServer.listen()

    while True:
        try:
            conn, info = socketServer.accept()
            conn.setblocking(False)
            t = threading.Thread(target=clientInput, args=([conn]))
            t.start()
            activeThreads += 1
            print("asdsa")
        except BlockingIOError:
            if newDataFromClients:
                star_time = time.time()
                if data:
                    print("Client:", requireClient["clientData"]["id"], "send data!")
                    if requireClient["clientData"]["id"] == None:
                        newSnake = Snake()
                        idPlayer = manager.addSnakeInGame(newSnake)
                        requireClient["socketClient"].sendall(pickle.dumps({"id": idPlayer}))
                    else:
                        if requireClient["clientData"]["key"] != None:
                            manager.userCommand(requireClient["clientData"]["key"], requireClient["clientData"]["id"])
                            manager.moveSnakes()
                            if manager.snakeDie(requireClient["clientData"]["id"]):
                                requireClient["socketClient"].sendall(pickle.dumps({"snakeStillInGame": False}))
                            else:
                                manager.checksAllSnakeEatFood()
                        else:
                            manager.romoveSnakeOnGame(requireClient["clientData"]["id"])
                            requireClient["socketClient"].close()
                    updateClients = True
                    newDataFromClients = False
                    doingLogicOfGame += (time.time() - star_time)

            if activeThreads == threadsThatAlreadyUpdateClients:
                threadsThatAlreadyUpdateClients = 0
                updateClients = False

