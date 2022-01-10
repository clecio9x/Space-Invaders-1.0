import pygame
from fire import Fire



# Este é a linha da programação do player1

class Player(pygame.sprite.Sprite):
    def __init__(self, posi, constraint,speed):
        super().__init__()
        self.image = pygame.image.load("./sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=posi)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 1100
        self.firer = pygame.sprite.Group()
        

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.fire()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
        

    def constraint(self):
        if self.rect.left <=0:
            self.rect.left = 0

        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def fire(self):
        self.firer.add(Fire(self.rect.center,-8,self.rect.bottom))
           #SFX Fire
        self.fire_sound = pygame.mixer.Sound("./sounds/laser.wav")
        self.fire_sound.set_volume(0.5)
        self.fire_sound.play()
        
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.firer.update()