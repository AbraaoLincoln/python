import pygame
import socket, pickle
import select
from snake.model.GameBoard import GameBoard
from snake.model.Player import Player
from snake.model.Snake import Snake
newPlayer = Player()

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12000        # The port used by the server

def drawSnakes(surface, snakes):
    for snake in snakes:
        snakeBody = snake["snakeBody"]
        snakeBodyColor = snake["snakeColors"][0]
        snakeHeadColor = snake["snakeColors"][1]
        for snakeBodypiece in snakeBody:
            pygame.draw.rect(surface, snakeBodyColor, [snakeBodypiece[0], snakeBodypiece[1], Snake.size, Snake.size])
        pygame.draw.rect(surface, snakeHeadColor, [snakeBody[-1][0], snakeBody[-1][1], Snake.size, Snake.size])

def drawFoods(surface, foods):
    for food in foods:
        pygame.draw.rect(surface, Snake.red, [food[0], food[1], Snake.size, Snake.size])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketClient:
    buffer = []
    socketClient.connect((HOST, PORT))
    #Solicita id para o servidor
    socketClient.sendall(pickle.dumps({"id": newPlayer.getId()}))
    socketClient.settimeout(0.1)
    #socketClient.setblocking(False)
    try:
        serverResponse = socketClient.recv(4096)
        buffer.append(serverResponse)
    except socket.timeout:
        print("timeout")

    if len(buffer) > 0:
        response = pickle.loads(b"".join(buffer))
        buffer.clear()
    newPlayer.setId(response["id"])

    if newPlayer.getId() != None:
        try:
            pygame.init()
        except:
            print("Não foi possivel iniciar o Pygame")

        gameScreen = pygame.display.set_mode((GameBoard.width, GameBoard.height))

        while newPlayer.getalive():

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    newPlayer.setAlive(False)
                    socketClient.sendall(pickle.dumps({"id": newPlayer.getId(), "key": None}))
                    socketClient.close()
                elif event.type == pygame.KEYDOWN:
                    socketClient.sendall(pickle.dumps({"id": newPlayer.getId(), "key": event.key}))
            if newPlayer.getalive():
                while True:
                    try:
                        serverResponse = socketClient.recv(4096)
                        buffer.append(serverResponse)
                        print(len(serverResponse))
                    except socket.timeout:
                        break
                if len(buffer) > 0:
                    response = pickle.loads(b"".join(buffer))
                    buffer.clear()
                    gameScreen.fill(Snake.black)
                    drawFoods(gameScreen, response["foods"])
                    drawSnakes(gameScreen, response["snakes"])
                pygame.display.update()
            else:
                print("Desconnect from the server!")

pygame.quit()