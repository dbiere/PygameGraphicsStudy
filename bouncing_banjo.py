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


class GameState():
    """
    Support ability to pause the game/demo
    """

    def __init__(self):
        self.active = True


class Banjo(pygame.sprite.Sprite):

    def __init__(self,
                 x_center = 200,
                 y_center = 200,
                 x_speed = 1,
                 y_speed = 1,
                 x_direction = 1,
                 y_direction = 1):
        super(Banjo, self).__init__()
        self.image = pygame.image.load('images/banjo.png').convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (x_center, y_center)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_direction = x_direction
        self.y_direction = y_direction

    def update(self):
        # Detect edges of window, reverse direction when hit
        if self.rect.top <= 0:
            self.y_direction = 1
        elif self.rect.bottom >= GameConstants.SCREEN_HEIGHT:
            self.y_direction = -1
        if self.rect.left <= 0:
            self.x_direction = 1
        elif self.rect.right >= GameConstants.SCREEN_WIDTH:
            self.x_direction = -1
        # Move it move it
        self.rect.x += self.x_direction * self.x_speed
        self.rect.y += self.y_direction * self.y_speed


def generate_random_banjo():
    """
    Generates an instance of the Banjo image/sprite at the center of the window
    moving at a random speed in a random direction
    """
    x_center = GameConstants.SCREEN_WIDTH / 2
    y_center = GameConstants.SCREEN_HEIGHT / 2
    # Set speed and direction
    x_speed = random.choice(range(GameConstants.MIN_SPEED, GameConstants.MAX_SPEED + 1, 1))
    y_speed = random.choice(range(GameConstants.MIN_SPEED, GameConstants.MAX_SPEED + 1, 1))
    x_direction = random.choice((-1, 1))
    y_direction = random.choice((-1, 1))
    return Banjo(
        x_center = x_center,
        y_center = y_center,
        x_direction = x_direction,
        y_direction = y_direction,
        x_speed = x_speed,
        y_speed = y_speed
    )

def main():

    pygame.init()

    state = GameState()

    screen = pygame.display.set_mode((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
    pygame.display.set_caption('Graphics Demo - Bouncing Banjo')
    clock = pygame.time.Clock()

    game_active = True

    # Sprites
    banjos = pygame.sprite.Group()
    banjos.add(generate_random_banjo())

    # Pause screen overlay
    pause_surface = pygame.Surface((GameConstants.SCREEN_WIDTH, GameConstants.SCREEN_HEIGHT))
    pause_surface.set_alpha(160) # 0 = transparent, 255 = opaque
    pause_surface.fill((0, 0, 0))

    # Game loop
    while game_active:

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and state.active:
                banjos.add(generate_random_banjo())
            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                if state.active: state.active = False
                else: state.active = True

        # Update sprites
        if state.active:
            banjos.update()

        # Render
        screen.fill(GameConstants.BACKGROUND_COLOR)
        banjos.draw(screen)
        if not state.active:
            # darken the screen
            screen.blit(pause_surface, (0, 0))

        pygame.display.update() # only after drawing everything else

        clock.tick(60)
    # End of main game loop

    pygame.quit()
    exit()

if __name__ == '__main__':
    main()
