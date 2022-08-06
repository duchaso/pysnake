import sys
from time import sleep
import pygame 
import random

pygame.init()


WIDTH = 800
HEIGHT = 400
SQUARE_S = 40

BOARD_W = int(WIDTH / SQUARE_S)
BOARD_H = int(HEIGHT / SQUARE_S)

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('PySnake')
clock = pygame.time.Clock()

# Draw net
rect_list = []
for y in range(0, HEIGHT, SQUARE_S):
    for x in range(0, WIDTH, SQUARE_S):
        rect_list.append(pygame.Rect(x, y, SQUARE_S, SQUARE_S))

class Apple:
    def __init__(self):
        self.c = (0 + SQUARE_S/2, 0 + SQUARE_S/2)
        self.r = SQUARE_S / 2
        self.color = (0, 255, 0)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.c, self.r)

    def update(self):
        x = random.randint(0, BOARD_W-1)
        y = random.randint(0, BOARD_H-1)
        self.c = (x * SQUARE_S + self.r, y * SQUARE_S + self.r)

    def center(self) -> tuple:
        return self.c

class Snake:
    def __init__(self):
        self.body = [
            (5, 5),
            (5, 6),
            (5, 7)
        ]

        self.head = [5 * SQUARE_S, 5 * SQUARE_S]
        self.speed = 2
        self.is_grow = False

        self.directions = {
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0)
        }
        self.direction = self.directions[pygame.K_UP]

    def grow(self):
        self.is_grow = True
    
    def head_rect(self) -> pygame.Rect:
        rect = self.body[0]
        return pygame.Rect(rect[0] * SQUARE_S, rect[1] * SQUARE_S, SQUARE_S, SQUARE_S)

    def update(self, key):
        user_dir = self.directions[key]
        if (user_dir[0] + self.direction[0], user_dir[1] + self.direction[1]) == (0, 0): return
        self.direction = self.directions[key]
    
    def move(self):
        self.head[0] += self.direction[0] * self.speed
        self.head[1] += self.direction[1] * self.speed 

        head = (self.head[0] // SQUARE_S, self.head[1] // SQUARE_S)


        if head != self.body[0]:
            if self.is_grow:
                self.is_grow = False
            else:
                del self.body[-1]
            self.body.insert(0, tuple(head))

    def draw(self, surface: pygame.Surface):
        for rect in self.body:
            pygame.draw.rect(surface, (0, 0, 255), pygame.Rect(rect[0] * SQUARE_S, rect[1] * SQUARE_S, SQUARE_S, SQUARE_S))

apple = Apple()
apple.update()
snake = Snake()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
                snake.update(event.key)
    screen.fill((0, 0, 0))

    for rect in rect_list:
        pygame.draw.rect(screen, (255, 255, 255), rect, width=1)

    snake.move()

    point = apple.center()
    if snake.head_rect().collidepoint(point[0], point[1]):
        apple.update()
        snake.grow()

    apple.draw(screen)
    snake.draw(screen)
    pygame.display.update()
    clock.tick(60)