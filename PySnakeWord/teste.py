import pygame
from random import randint
import time
try:
    pygame.init()
except:
    print("Erro ao iniciar o pygame")


width = 640
height = 480
#Abre uma janela com a largura e altura passado como um tupla.
background = pygame.display.set_mode( (width, height) )
#Defini um titulo para a jenela aberta acima.
pygame.display.set_caption("Teste de titulo!")

exit = True
size = 10
posX_init_snake = randint(0, (width-size)/10)*10
posY_init_snake = randint(0, (height-size)/10)*10
posX_init_apple = randint(0, (width-size)/10)*10
posY_init_apple = randint(0, (height-size)/10)*10
rect_snake = [posX_init_snake, posY_init_snake, size, size]
rect_apple = [posX_init_apple, posY_init_apple, size, size]
speedX = 0
speedY = 0
timeR = pygame.time.Clock()
snake_length = 1
snake = []
#snake = [[posX_init_snake, posY_init_snake]]
#snake.append([posX_init_snake, posY_init_snake])

def drawSnake(snakeBody):
    for snake_piece in snakeBody:
        pygame.draw.rect(background, (0, 0, 0), [snake_piece[0], snake_piece[1], size, size])

def drawApple():
    pygame.draw.rect(background, (178, 34, 34), rect_apple)

while exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                speedX = size
                speedY = 0
            elif event.key == pygame.K_LEFT:
                speedX = -size
                speedY = 0
            elif event.key == pygame.K_UP:
                speedX = 0
                speedY = -size
            elif event.key == pygame.K_DOWN:
                speedX = 0
                speedY = size
        #print(event)
    posX_init_snake += speedX
    posY_init_snake += speedY
    new_snake_peice = []
    new_snake_peice.append(posX_init_snake)
    new_snake_peice.append(posY_init_snake)
    snake.append(new_snake_peice)
    background.fill((255, 255, 255))
    if posX_init_snake == rect_apple[0] and posY_init_snake == rect_apple[1]:
        rect_apple[0] = randint(0, (width - size)/10)*10
        rect_apple[1] = randint(0, (height - size)/10)*10
        snake_length += 1

    if len(snake) > snake_length:
        del snake[0]
    drawSnake(snake)
    drawApple()
    pygame.display.update()
    pygame.display.update()
    timeR.tick(10)
    #Setando a logica da borda
    #borda da horizontal(eixo x)
    if posX_init_snake >= width:
        posX_init_snake = 0
    elif posX_init_snake < 0:
        posX_init_snake = width - size
    #borda da vertical(eixo y)
    if posY_init_snake >= height:
        posY_init_snake = 0
    elif posY_init_snake < 0:
        posY_init_snake = height - size


#Encerra o programa e fecha a janela.
pygame.quit()