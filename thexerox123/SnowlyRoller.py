import pygame
import spritesheet
import itertools
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Game:
    def __init__(self) -> None:
        self.window_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snowly Roller")
        self.x = 500.0
        self.y = 500.0
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.init_time = pygame.time.get_ticks()
        self.player = spritesheet.Player()
        self.snowball = spritesheet.Snowball()
        self.terrain = spritesheet.Terrain()
        self.grass = pygame.image.load('images/Grass.png').convert_alpha()

    def setup_background(self): 
        self.window_surface.blit(self.terrain.land_list[self.terrain.landframe], (162, 90)) 
        brick_width, brick_height = self.terrain.land_list[self.terrain.landframe].get_width(), self.terrain.land_list[self.terrain.landframe].get_height()
        for self.x,self.y in itertools.product(range(0,1920+1,brick_width), range(0,1080+1,brick_height)):
            self.window_surface.blit(self.terrain.land_list[self.terrain.landframe], (self.x, self.y))  

    def run(self):
        running = True
        while running:
            # drawing stuff
            self.window_surface.blit(self.grass, (0, 0))
            self.setup_background()
            self.window_surface.blit(self.player.animation_list[self.player.action][self.player.frame], (self.x, y))
            self.window_surface.blit(self.snowball.snow_list[self.snowball.frame], (self.x + self.snowball.x, y + self.snowball.y))
            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.player.is_moving = False
                        self.player.frame = 0
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_UP:
                        self.player.action = 1
                        self.player.frame = 0
                        self.snowball.x = 17
                        self.snowball.y = -12
                    if event.key == K_LEFT:
                        self.player.action = 2
                        self.player.frame = 0
                        self.snowball.x = -22
                        self.snowball.y = 23
                    if event.key == K_DOWN:
                        self.player.action = 3
                        self.player.frame = 0
                        self.snowball.x = 22
                        self.snowball.y = 62
                    if event.key == K_RIGHT:
                        self.player.action = 0
                        self.player.frame = 0
                        self.snowball.x = 65
                        self.snowball.y = 24  
                elif event.type == QUIT:
                    running = False 

            key_pressed_is = pygame.key.get_pressed()   
            if key_pressed_is[K_LEFT] and self.x > 200:
                self.x -= 10
                self.player.is_moving = True
            if key_pressed_is[K_RIGHT] and self.x < 1640:
                self.x += 10
                self.player.is_moving = True
            if key_pressed_is[K_UP] and y > 100:
                self.y -= 10
                self.player.is_moving = True
            if key_pressed_is[K_DOWN] and y < 880:
                self.y += 10
                self.player.is_moving = True   

            current_time = pygame.time.get_ticks()
            if current_time - self.init_time >= self.player.animation_cooldown:
                if self.player.is_moving:
                    self.player.frame += 1
                    self.snowball.frame += 1
                    self.init_time = current_time
                    if self.player.frame >= len(self.player.animation_list[self.player.action]):
                        self.player.frame = 0
                    if self.snowball.frame >= len(self.snowball.snow_list):
                        self.snowball.frame = 0   

            self.clock.tick(self.fps)
            pygame.display.update() 
        pygame.quit()   


    def update(self):
        # This function should be called for every loop through the main game loop.
        # It should tell every object to update itself.
        # You may end up needing to pass variables to the objects for them to update properly. For instance, player inputs.
        pass

    def draw(self):
        # This function should be called every loop through the main game loop.
        # This should tell every object to draw itself.
        # You may have to pass the surface you want objects to draw themselves on to.
        pass


if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
    pygame.init()
    Game()