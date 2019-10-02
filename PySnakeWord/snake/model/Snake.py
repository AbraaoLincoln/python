import pygame
from random import randrange

from snake.model.GameBoard import GameBoard

class Snake:

    #Static variaveis
    snakeInitSize = 3
    size = 10
    #Construtor
    def __init__(self):
        self.snakeBody = []
        self.active = True
        #self.idSnake = id
        self.snakeColor = (65, 147, 166)
        self.snakeHeadColor = (255, 200, 87)
        self.snakeHeadeX = randrange(0, GameBoard.width, Snake.size)
        self.snakeHeadeY = randrange(0, GameBoard.height, Snake.size)
        self.snakeBody.append([self.snakeHeadeX, self.snakeHeadeY])
        self.snakeBody.append([self.snakeHeadeX + Snake.size, self.snakeHeadeY])
        self.snakeBody.append([self.snakeHeadeX + Snake.size * 2, self.snakeHeadeY])
        self.speedX = 0
        self.speedY = 0
        self.snakeLength = 3
        #Snake.snakeInGame += 1

    def getSnake(self):
        return self.snakeBody

    def growSnake(self, newBodyPiece):
        self.snakeBody.append(newBodyPiece)

    def drawSnake(self, surface):
        #Desenha a snake na surface passada como paramentro.
        for eachPiece in self.snakeBody:
            pygame.draw.rect(surface, self.snakeColor, [eachPiece[0], eachPiece[1], Snake.size, Snake.size])
        pygame.draw.rect(surface, self.snakeHeadColor, [self.snakeBody[-1][0], self.snakeBody[-1][1], Snake.size, Snake.size])

    def incrementSpeedX(self, increment):
        self.speedX = increment

    def incrementSpeedY(self, increment):
        self.speedY = increment

    def getSpeedX(self):
        return self.speedX

    def getSpeedY(self):
        return self.speedY

    def getHaedSnake(self):
        return self.snakeBody[-1]

    def moveSnake(self):
        if len(self.snakeBody) > self.snakeLength:
            del self.snakeBody[0]
        #print(self.snakeBody)
        newPosXHeadSnake = self.snakeBody[-1][0] + self.speedX
        newPosYHeadSnake = self.snakeBody[-1][1] + self.speedY
        self.snakeBody.append([newPosXHeadSnake, newPosYHeadSnake])

    def throughTheBoard(self, vertical, right, up):
        del self.snakeBody[0]
        if vertical:
            if right:
                newPosXHeadSnake = 0
                newPosYHeadSnake = self.snakeBody[-1][1]
            else:
                newPosXHeadSnake = GameBoard.width - Snake.size
                newPosYHeadSnake = self.snakeBody[-1][1]
        else:
            if up:
                newPosXHeadSnake = self.snakeBody[-1][0]
                newPosYHeadSnake = GameBoard.height - Snake.size
            else:
                newPosXHeadSnake = self.snakeBody[-1][0]
                newPosYHeadSnake = 0
        self.snakeBody.append([newPosXHeadSnake, newPosYHeadSnake])

    def increaseSnakeLength(self):
        self.snakeLength += 1