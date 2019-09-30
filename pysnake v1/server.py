import pygame
#import sys
#sys.path.append('~/PycharmProjects/pygames')
#print(sys.path)
from snake.model.Snake import Snake
from snake.model.GameBoard import GameBoard
from snake.controle.GameManeger import GameManeger

try:
    pygame.init()
except:
    print("falha ao iniciar o pygame")

#abre a janela.
surfaceGame = pygame.display.set_mode((GameBoard.width, GameBoard.height))
exit = True
timer = pygame.time.Clock()
#Testes
snake1 = Snake(0)
maneger = GameManeger()
maneger.addSnakeInGame(snake1)

while exit:
    surfaceGame.fill((9, 10, 13))
    maneger.initGame(surfaceGame)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit = False
        else:
            maneger.commandToSnake(e, 0)
    maneger.moveSnakes(surfaceGame)
    maneger.checksSnakeEatFood()
    timer.tick(15)
    pygame.display.update()

pygame.quit()