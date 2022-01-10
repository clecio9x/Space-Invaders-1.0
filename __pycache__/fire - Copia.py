import pygame

class Fire(pygame.sprite.Sprite):
    def __init__(self,posi,speed,height):
        super().__init__()
        self.image = pygame.Surface((6,40))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = posi)
        self.speed = speed
        self.height_y_constraint = height
    

    def endfire(self):
       if self.rect.y <= -100 or self.rect.y >= self.height_y_constraint + 100:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.endfire()