import pygame, random, sys
from pygame import mixer
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.headUp = pygame.image.load('head_up.jpg').convert_alpha()
        self.headDown = pygame.image.load('head_down.jpg').convert_alpha()
        self.headLeft = pygame.image.load('head_left.jpg').convert_alpha()
        self.headRight = pygame.image.load('head_right.jpg').convert_alpha()

        self.tailUp = pygame.image.load('tail_up.jpg').convert_alpha()
        self.tailDown = pygame.image.load('tail_down.jpg').convert_alpha()
        self.tailRight = pygame.image.load('tail_right.jpg').convert_alpha()
        self.tailLeft = pygame.image.load('tail_left.jpg').convert_alpha()

        self.bodyHr = pygame.image.load('body_hr.jpg').convert_alpha()
        self.bodyVr = pygame.image.load('body_vr.jpg').convert_alpha()

        self.bodyTr = pygame.image.load('body_tr.jpg').convert_alpha()
        self.bodyTl = pygame.image.load('body_tl.jpg').convert_alpha()
        self.bodyBr = pygame.image.load('body_br.jpg').convert_alpha()
        self.bodyBl = pygame.image.load('body_bl.jpg').convert_alpha()
        self.sound = mixer.Sound('applecrunch.wav')

    def draw_snake(self):

        for index, block in enumerate(self.body):
            snake_X = int(block.x * grid_size)
            snake_Y = int(block.y * grid_size)
            snake = pygame.Rect(snake_X, snake_Y, grid_size, grid_size)
            self.head = self.headRight
            self.tail = self.tailRight

            if index == 0:
                self.update_head()
                screen.blit(self.head, snake)
            elif index == len(self.body) - 1:
                self.update_tail()
                screen.blit(self.tail, snake)
            else:
                prev_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.bodyVr, snake)
                elif prev_block.y == next_block.y:
                    screen.blit(self.bodyHr, snake)
                else:
                    if (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
                        screen.blit(self.bodyTl, snake)
                    if (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
                        screen.blit(self.bodyBl, snake)
                    if (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
                        screen.blit(self.bodyTr, snake)
                    if (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1):
                        screen.blit(self.bodyBr, snake)

    def update_head(self):
        head_side = self.body[1] - self.body[0]
        if head_side == Vector2(1, 0):
            self.head = self.headLeft
        elif head_side == Vector2(-1, 0):
            self.head = self.headRight
        elif head_side == Vector2(0, 1):
            self.head = self.headUp
        elif head_side == Vector2(0, -1):
            self.head = self.headDown

    def update_tail(self):
        tail_side = self.body[-2] - self.body[-1]
        if tail_side == Vector2(1, 0):
            self.tail = self.tailLeft
        if tail_side == Vector2(-11, 0):
            self.tail = self.tailRight
        if tail_side == Vector2(0, 1):
            self.tail = self.tailUp
        if tail_side == Vector2(0, -1):
            self.tail = self.tailDown

    def move_snake(self):
        if self.new_block == True:
            snake_copy = self.body[:]
            snake_copy.insert(0, snake_copy[0] + self.direction)
            self.body = snake_copy[:]
            self.new_block = False
        else:
            snake_copy = self.body[:-1]
            snake_copy.insert(0, snake_copy[0] + self.direction)
            self.body = snake_copy[:]

    def add_block(self):
        self.new_block = True

    def playsound(self):
        self.sound.play()
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)



class Apple:
    def __init__(self):
        self.change_pos()

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x * grid_size), int(self.pos.y * grid_size), grid_size, grid_size)
        screen.blit(apple, apple_rect)
        # pygame.draw.rect(screen, (126, 166, 114), apple)

    def change_pos(self):
        self.apple_X = random.randint(0, grid_number - 1)
        self.apple_Y = random.randint(0, grid_number - 1)
        self.pos = Vector2(self.apple_X, self.apple_Y)


class RUN:
    def __init__(self):
        self.apple = Apple()
        self.snake = Snake()
        self.score_value = 0

    def update(self):

        self.snake.move_snake()
        self.collision()
        self.check_game_over()

    def draw(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.apple.draw_apple()
        self.score()

    def collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.score_value += 1
            self.snake.playsound()
            self.apple.change_pos()
            self.snake.add_block()
        for block in self.snake.body[1:]:
            if block == self.apple.pos:
                self.apple.change_pos()

    def check_game_over(self):
        if (not 0 <= self.snake.body[0].x < grid_number) or (not 0 <= self.snake.body[0].y < grid_number):
            self.gameover()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameover()

    def gameover(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(grid_number):
            if row % 2 == 0:
                for column in range(grid_number):
                    if column % 2 == 0:
                        grass_rect = pygame.Rect(column * grid_size, row * grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for column in range(grid_number):
                    if column % 2 != 0:
                        grass_rect = pygame.Rect(column * grid_size, row * grid_size, grid_size, grid_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def score(self):
        score_Value = len(self.snake.body) - 3
        score = gameFont.render(str(score_Value), True, (46, 74, 12))
        score_rect = score.get_rect(center=(textX, textY))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        # container = pygame.Rect(apple_rect.left, apple_rect.topright, apple_rect.width + score_rect.width ,apple_rect.height)

        # pygame.draw.rect(screen, (167, 209, 61), container)
        screen.blit(score, score_rect)
        screen.blit(apple, apple_rect)
        # pygame.draw.rect(screen, (167, 209, 61), container,2)


pygame.init()

# for title and icon
pygame.display.set_caption("Snake Game")
icon = pygame.image.load('anaconda.png')
pygame.display.set_icon(icon)
# for screen
grid_size = 40
grid_number = 15
screen = pygame.display.set_mode((grid_number * grid_size, grid_number * grid_size))
clock = pygame.time.Clock()

# for apple image
apple = pygame.image.load('apple1.png').convert_alpha()

# for font
gameFont = pygame.font.Font('game.ttf', 25)
textX = int(grid_size * grid_number - 60)
textY = int(grid_size * grid_number - 40)

# for movement
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

game = RUN()
running = True
while running:
    screen.fill((175, 215, 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction.x != - 1:
                game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_UP and game.snake.direction.y != 1:
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction.y != - 1:
                game.snake.direction = Vector2(0, 1)

    game.draw()

    pygame.display.update()
    clock.tick(60)
