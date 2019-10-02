import pygame
import socket, pickle
import select
from snake.model.GameBoard import GameBoard
from snake.model.Player import Player
newPlayer = Player()

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketClient:
    buffer = []
    socketClient.connect((HOST, PORT))
    #Solicita id para o servidor
    socketClient.sendall(pickle.dumps({"id": newPlayer.getId()}))
    socketClient.settimeout(0.1)
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
                elif event.type == pygame.KEYDOWN:
                    socketClient.sendall(pickle.dumps({"id": newPlayer.getId(), "key": event.key}))
            #r, w, e = select.select([socketClient], [], [])
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

pygame.quit()