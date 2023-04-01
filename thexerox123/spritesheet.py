import pygame   


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet_surface = pygame.image.load('images/master.png').convert_alpha()
        self.rect = self.sprite_sheet_surface.get_rect()
        self.is_moving = False
        self.step_counter = 0
        self.animation_cooldown = 125
        self.action = 0
        self.animation_list = []
        self.animation_steps = [12, 12, 12, 12]
        self.frame = 0
        self.load_animation_list()

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet_surface, (0, 0), ((frame * width), 0, width, height))
        self.rect = (self.sprite_sheet_surface, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image

    def load_animation_list(self):
        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(self.get_image(self.step_counter, 32, 32, 3, (0, 0, 0)))
                self.step_counter += 1
            self.animation_list.append(temp_img_list)

    def update(self):
        # This is where the code for updating the indices for the player should live.
        pass

    def draw(self):
        # This is where the player should be drawing itself onto the surface. 
        # You may need to have the game pass the main window surface here as a variable.
        pass


class Snowball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet_surface = pygame.image.load('images/snowball.png').convert_alpha()
        self.rect = self.sprite_sheet_surface.get_rect()
        self.x = 65
        self.y = 24
        self.spheresize = 0.1
        self.frame = 0
        self.snow_list = []
        self.snow_steps = 5
        self.load_animation_list()

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet_surface, (0, 0), ((frame * width), 0, width, height))
        self.rect = (self.sprite_sheet_surface, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        return image
    
    def load_animation_list(self):
        for snow in range(self.snow_steps):
            self.snow_list.append(self.get_image(snow, 416, 450, self.spheresize, (0, 0, 0)))

    def update(self):
        pass

    def draw(self):
        pass


class Terrain(pygame.sprite.Sprite):
    def __init__(self):
        self.sprite_sheet_surface = pygame.image.load('images/land.png').convert_alpha() 
        self.rect = self.sprite_sheet_surface.get_rect()
        self.landframe = 0
        self.land_list = []
        self.land_steps = 9
        self.load_animation_list()

    def get_image(self, frame, width, height, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet_surface, (0, 0), ((frame * width), 0, width, height))
        image.set_colorkey(colour)
        return image    

    def load_animation_list(self):
        for land in range(self.land_steps):
            self.land_list.append(self.get_image(land, 150, 180, (0, 0, 0)))

    def update(self):
        pass

    def draw(self):
        pass