import pygame
import socket, pickle

from snake.model.GameBoard import GameBoard
from snake.model.Player import Player
newPlayer = Player()

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketClient:
    #Conectando com o servidor e recebendo o id e a tela atual do jogo.
    #socketClient.setblocking(0)
    socketClient.connect((HOST, PORT))
    socketClient.sendall(pickle.dumps({"id": newPlayer.getId()}))
    socketClient.settimeout(0.7)
    buffer = []
    while True:
        # serverResponse = socketClient.recv(4096)
        # if not serverResponse:
        #     break
        # else:
        #     buffer.append(serverResponse)
        try:
            serverResponse = socketClient.recv(4096)
            buffer.append(serverResponse)
        except socket.timeout:
            break
    if len(buffer) > 0:
        response = pickle.loads(b"".join(buffer))
        buffer.clear()
    #print(len(buffer))
    newPlayer.setId(response["id"])

    if newPlayer.getId() != None:
        try:
            pygame.init()
        except:
            print("Não foi possivel iniciar o Pygame")

        gameScreen = pygame.display.set_mode((GameBoard.width, GameBoard.height))
        gameScreen.blit(pygame.image.fromstring(response["gameScreen"][0], response["gameScreen"][1], "RGB"), (0, 0))

        while newPlayer.getalive():

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    newPlayer.setAlive(False)
                elif event.type == pygame.KEYDOWN:
                    socketClient.sendall(pickle.dumps({"id": newPlayer.getId(), "key": event.key}))

                    while True:
                        try:
                            serverResponse = socketClient.recv(4096)
                            buffer.append(serverResponse)
                        except socket.timeout:
                            break
                    if len(buffer) > 0:
                        response = pickle.loads(b"".join(buffer))
                        buffer.clear()
                        gameScreen.blit(pygame.image.fromstring(response[0], response[1], "RGB"), (0, 0))

            pygame.display.update()
