import pygame
import sys,random
import os
from pygame.math import Vector2

pygame.init()

cell_size = 40
cell_number = 20


SCREEN = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
FPS = 60

apple_img = pygame.image.load(os.path.join('Assets' , 'apple.png'))
apple = pygame.transform.scale(apple_img,(cell_size,cell_size))
mouse_img = pygame.image.load(os.path.join('Assets' , 'mouse.png'))
mouse = pygame.transform.scale(mouse_img,(cell_size,cell_size))

font = pygame.font.Font('Assets/Font/PoetsenOne-Regular.ttf', 25)
crunch_sound = pygame.mixer.Sound('Assets/Sound/crunch.wav')
gameover_sound = pygame.mixer.Sound('Assets/Sound/gameover.wav')


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.count = 0

    def update(self):
        self.snake.move()
        self.eat()
        self.gameover()

    def draw(self):
        self.count = self.count + 1
        self.backgrd()
        self.fruit.draw_fruit()
        self.snake.draw()
        self.score()

    def eat(self):
        if self.fruit.pos == self.snake.body[0]:
            # add snake length
            # place another fruit
            self.fruit.place()
            self.snake.addlen()
            crunch_sound.play()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.place()   # prevents from placing on snake

    def backgrd(self):
        grass_color = (0,245,0)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(SCREEN, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(SCREEN, grass_color, grass_rect)

    def gameover(self):
        # check snake hits itself
        # snake is out of screen
        if not 0 <= self.snake.body[0].x < cell_number:
            self.dead()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.dead()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.dead()

    def dead(self):
        self.snake.reset()


    def score(self):
        score_text = str(len(self.snake.body) - 3)
        score_font = font.render(score_text,1,(56,74,12))
        x = cell_size * cell_number - 60
        y = cell_size * cell_number - 40
        score_rect = score_font.get_rect(center =(x,y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.w + score_rect.w + 10,apple_rect.height)
        pygame.draw.rect(SCREEN,(77,255,77),bg_rect)
        pygame.draw.rect(SCREEN, (56,74,12), bg_rect,2)

        SCREEN.blit(score_font, score_rect)
        SCREEN.blit(apple, apple_rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.newblock = False

        self.head_up = pygame.image.load('Assets/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Assets/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Assets/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Assets/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Assets/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Assets/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Assets/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Assets/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Assets/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Assets/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Assets/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Assets/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Assets/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Assets/body_bl.png').convert_alpha()

    def draw(self):
        self.update_head_image()
        self.update_tail_image()
        for index,block in enumerate(self.body):
            rect = pygame.Rect(block.x * cell_size,block.y* cell_size,cell_size,cell_size)
            if index == 0:
                SCREEN.blit(self.head,rect)
            elif index == len(self.body) - 1:
                SCREEN.blit(self.tail,rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    SCREEN.blit(self.body_vertical,rect)
                elif previous_block.y == next_block.y:
                    SCREEN.blit(self.body_horizontal,rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        SCREEN.blit(self.body_tl,rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        SCREEN.blit(self.body_bl,rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        SCREEN.blit(self.body_tr,rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        SCREEN.blit(self.body_br,rect)

    def update_head_image(self):
        head_direction = self.body[1] - self.body[0]
        if head_direction == Vector2(1, 0):
            self.head = self.head_left
        elif head_direction == Vector2(-1, 0):
            self.head = self.head_right
        elif head_direction == Vector2(0, 1):
            self.head = self.head_up
        elif head_direction == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_image(self):
        tail_direction = self.body[len(self.body)-2] - self.body[len(self.body)-1]
        if tail_direction == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_direction == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_direction == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_direction == Vector2(0, -1):
            self.tail = self.tail_down

    def move(self):
        if self.newblock:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newblock = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def addlen(self):
        self.newblock = True

    def reset(self):

        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,120)

class Fruit:
    def __init__(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

    def draw_fruit(self):
        rect = pygame.Rect(self.pos.x * cell_size,cell_size * self.pos.y,cell_size,cell_size)
        # pygame.draw.rect(SCREEN,rect)
        SCREEN.blit(apple,(rect.x,rect.y))

    def place(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)



main = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0,1)

            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1,0)

            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1,0)
    SCREEN.fill(pygame.Color((77,255,77)))
    main.draw()

    pygame.display.update()
    clock.tick(FPS)
