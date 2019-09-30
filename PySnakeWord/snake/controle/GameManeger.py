import pygame

from snake.model.Snake import Snake
from snake.model.GameBoard import GameBoard
from snake.model.Food import Food

class GameManeger:

    #Variaveis staticas
    #snakeInGame = []

    #Construtor
    def __init__(self, surface):
        self.snakeInGame = []
        self.food = Food()
        self.gameSurface = surface

    def addSnakeInGame(self, newSnake):
        self.snakeInGame.append(newSnake)
        return len(self.snakeInGame) - 1

    def romoveSnakeOnGame(self, idSnake):
        del self.snakeInGame[idSnake]

    def commandToSnake(self, userInput, idSnake):
        if userInput.type == pygame.KEYDOWN:
            if userInput.key == pygame.K_UP and self.snakeInGame[idSnake].getSpeedY() != Snake.size:
                self.snakeInGame[idSnake].incrementSpeedY(-Snake.size)
                self.snakeInGame[idSnake].incrementSpeedX(0)
            elif userInput.key == pygame.K_DOWN and self.snakeInGame[idSnake].getSpeedY() != -Snake.size:
                self.snakeInGame[idSnake].incrementSpeedY(Snake.size)
                self.snakeInGame[idSnake].incrementSpeedX(0)
            elif userInput.key == pygame.K_RIGHT and self.snakeInGame[idSnake].getSpeedX() != -Snake.size:
                self.snakeInGame[idSnake].incrementSpeedY(0)
                self.snakeInGame[idSnake].incrementSpeedX(Snake.size)
            elif userInput.key == pygame.K_LEFT and self.snakeInGame[idSnake].getSpeedX() != Snake.size:
                self.snakeInGame[idSnake].incrementSpeedY(0)
                self.snakeInGame[idSnake].incrementSpeedX(-Snake.size)

    def userCommand(self, userInput, idSnake):
        if userInput == pygame.K_UP and self.snakeInGame[idSnake].getSpeedY() != Snake.size:
            self.snakeInGame[idSnake].incrementSpeedY(-Snake.size)
            self.snakeInGame[idSnake].incrementSpeedX(0)
        elif userInput == pygame.K_DOWN and self.snakeInGame[idSnake].getSpeedY() != -Snake.size:
            self.snakeInGame[idSnake].incrementSpeedY(Snake.size)
            self.snakeInGame[idSnake].incrementSpeedX(0)
        elif userInput == pygame.K_RIGHT and self.snakeInGame[idSnake].getSpeedX() != -Snake.size:
            self.snakeInGame[idSnake].incrementSpeedY(0)
            self.snakeInGame[idSnake].incrementSpeedX(Snake.size)
        elif userInput == pygame.K_LEFT and self.snakeInGame[idSnake].getSpeedX() != Snake.size:
            self.snakeInGame[idSnake].incrementSpeedY(0)
            self.snakeInGame[idSnake].incrementSpeedX(-Snake.size)

    def moveSnakes(self, surface):
        for snake in self.snakeInGame:
            snakeHead = snake.getHaedSnake()
            if snakeHead[0] > GameBoard.width:
                snake.throughTheBoard(True, True, None)
            elif snakeHead[0] < 0:
                snake.throughTheBoard(True, False, None)
            elif snakeHead[1] > GameBoard.height:
                snake.throughTheBoard(False, None, False)
            elif snakeHead[1] < 0:
                snake.throughTheBoard(False, None, True)
            snake.moveSnake()
            snake.drawSnake(surface)

    def checksSnakeEatFood(self):
        for snake in self.snakeInGame:
            snakeHead = snake.getHaedSnake()
            foodPosition = self.food.getFoodPosition()
            if snakeHead[0] == foodPosition[0] and snakeHead[1] == foodPosition[1]:
                snake.increaseSnakeLength()
                self.food.generateNewFood()
                break


    def initGame(self, surface):
        self.food.drawFood(surface)

    def sendSruface(self):
        return (pygame.image.tostring(self.gameSurface, "RGB"), self.gameSurface.get_size())