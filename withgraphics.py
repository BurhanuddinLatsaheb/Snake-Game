import pygame, random, sys
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(4, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            snake_X = int(block.x * grid_size)
            snake_Y = int(block.y * grid_size)
            snake = pygame.Rect(snake_X, snake_Y, grid_size, grid_size)
            pygame.draw.rect(screen, (255, 215, 0), snake)

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


class Apple:
    def __init__(self):
        self.change_pos()

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x * grid_size), int(self.pos.y * grid_size), grid_size, grid_size)
        pygame.draw.rect(screen, (126, 166, 114), apple_rect)

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
        self.snake.draw_snake()
        self.apple.draw_apple()

    def collision(self):
        if self.apple.pos == self.snake.body[0]:
            self.score_value += 1
            self.apple.change_pos()
            self.snake.add_block()

    def check_game_over(self):
        if (not 0 <= self.snake.body[0].x < grid_number) or (not 0 <= self.snake.body[0].y < grid_number):
            pygame.quit()
            sys.exit()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                pygame.quit()
                sys.exit()


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
print("with graphics")
