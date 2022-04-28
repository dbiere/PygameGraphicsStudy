# Pygame graphics learning demo using Sprites
# With every press of spacebar, produces a picture of my dog Banjo
# moving from the center of the screen in a random direction at a
# random speed. The pictures bounce off the edge of the screen.

import pygame
import random

class GameConstants():
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    BACKGROUND_COLOR = (255, 255, 255)
    MIN_SPEED = 1
    MAX_SPEED = 5

class Banjo(pygame.sprite.Sprite):
    def __init__(self,
                 x_speed=1,
                 y_speed=1,
                 x_direction=1,
                 y_direction=1):
        super(Banjo, self).__init__()
        self.image = pygame.image.load('images/banjo.png').convert_alpha()
        #self.image = pygame.transform.rotozoom(self.image, 0, .25)
        self.image = pygame.transform.smoothscale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = ((GameConstants.SCREEN_WIDTH / 2, GameConstants.SCREEN_HEIGHT / 2))

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.x_direction = x_direction
        self.y_direction = y_direction

    def update(self):

        # Detect hitting top or bottom
        if self.rect.top <= 0:
            self.y_direction = 1
        elif self.rect.bottom >= GameConstants.SCREEN_HEIGHT:
            self.y_direction = -1
        # Detect hitting left or right
        if self.rect.left <= 0:
            self.x_direction = 1
        elif self.rect.right >= GameConstants.SCREEN_WIDTH:
            self.x_direction = -1

        # Move it
        self.rect.x += self.x_direction * self.x_speed
        self.rect.y += self.y_direction * self.y_speed

def generate_random_banjo():

    # set speed
    x_speed = random.choice(range(GameConstants.MIN_SPEED, GameConstants.MAX_SPEED + 1, 1))
    y_speed = random.choice(range(GameConstants.MIN_SPEED, GameConstants.MAX_SPEED + 1, 1))

    # set direction, either 1 (down or right) or -1 (up or left)
    x_direction = random.choice((-1, 1))
    y_direction = random.choice((-1, 1))

    return Banjo(
        x_direction = x_direction,
        y_direction = y_direction,
        x_speed = x_speed,
        y_speed = y_speed
    )

def main():

    pygame.init()

    screen = pygame.display.set_mode((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
    pygame.display.set_caption('Graphics Demo - Bouncing Banjo')
    clock = pygame.time.Clock()

    game_running = True

    # Sprites
    banjos = pygame.sprite.Group()
    banjos.add(generate_random_banjo())

    # Game loop
    while game_running:

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                banjos.add(generate_random_banjo())

        # Update
        banjos.update()

        # Render
        screen.fill(GameConstants.BACKGROUND_COLOR)
        banjos.draw(screen)
        pygame.display.update() # after drawing everything

        clock.tick(60)

    pygame.quit()
    exit()

if __name__ == '__main__':
    main()
