import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_patch = "./sprites/" + color + ".png"
        self.image = pygame.image.load(file_patch).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == "red":self.value = 20
        elif color =="yellow":self.value = 30
        else: self.value = 50

    def update(self,direct):
        self.rect.x += direct

class Alien_extra(pygame.sprite.Sprite):
    def __init__(self,side,width):
        super().__init__()
        file_patch = "./sprites/extra.png"
        self.image = pygame.image.load(file_patch).convert_alpha()
        if side == "right":
            x = width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,80))
    def update(self):
        self.rect.x += self.speed
