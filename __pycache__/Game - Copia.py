import sys
import pygame
from player1 import Player
import wall
from aliens import Alien, Alien_extra
from random import choice, randint
from fire import Fire

# Cor de fundo
background_color = [0, 0, 0]

# Titulo da janela
title = "Space Invaders"

class Game:
    def __init__(self):
        #Player
        player_sprite = Player((width / 2, height),width,10)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.player.firer = pygame.sprite.GroupSingle()
        #player lives
        self.lives = 3
        self.live_surf = pygame.image.load("./sprites/player.png").convert_alpha()
        self.live_x_start_position = width - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("./sprites/Pixeled.ttf",20)
        

        #Wall
        self.shape = wall.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.wall_amount = 4
        self.wall_positions = [num * (width / self.wall_amount) for num in range(self.wall_amount)]
        self.multiple_wall(*self.wall_positions,x_start = 64,y_start = 580) #or width / 15

        #Aliens
        self.alien = pygame.sprite.Group()
        self.alien_fire = pygame.sprite.Group()
        self.alien_setup(rows = 5, cols = 11)
        self.dificult_speed = 1
        self.alien.direct = self.dificult_speed
        
        
        #Alien Extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)

    def create_wall(self,x_start,y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = wall.Wall(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def multiple_wall(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_wall(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_dis = 60,y_dis = 48,x_offset = 70, y_offset = 100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dis + x_offset
                y = row_index * y_dis + y_offset
                if row_index == 0: alien_sprite = Alien("green",x,y)
                elif 1<= row_index <= 2: alien_sprite = Alien("yellow",x,y)
                else: alien_sprite = Alien("red",x,y)
                self.alien.add(alien_sprite)
    
    def alien_position_check(self):
        all_aliens = self.alien.sprites()
        for alien in all_aliens:
            if alien.rect.right >= width:
                self.alien.direct =  self.dificult_speed * -1
                self.alien_move_down(1)
            elif alien.rect.left <= 0:
                self.alien.direct = self.dificult_speed
                self.alien_move_down(1)
            
        

    def alien_move_down(self,down):
        if self.alien:
            for alien in self.alien.sprites():
                alien.rect.y += down
    
    def alien_shoot(self):
        if self.alien.sprites():
            randon_alien = choice(self.alien.sprites())
            fire_alien = Fire(randon_alien.rect.center,6,height)
            self.alien_fire.add(fire_alien)
            

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <=0:
            self.extra.add(Alien_extra(choice(["right","left"]),width))
            self.extra_spawn_time = randint(400,800)
    
    # SFX
        self.alien_hit_sound = pygame.mixer.Sound("./sounds/alien_hit.wav")
        self.alien_hit_sound.set_volume(0.3)
        self.alien_extra_hit_sound = pygame.mixer.Sound("./sounds/alien_extra_hit.wav")
        self.alien_extra_hit_sound.set_volume(0.5)
        self.player_hit_sound = pygame.mixer.Sound("./sounds/dead.wav")
        self.player_hit_sound.set_volume(0.5)

    def collisions_event(self):
        #player fire
        if self.player.sprite.firer:
            for fire in self.player.sprite.firer:
                #obstacle hit
                if pygame.sprite.spritecollide(fire,self.blocks,True):
                    fire.kill()
 
                #alien hit
                alien_hit = pygame.sprite.spritecollide(fire,self.alien,True)
                if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.value
                        fire.kill()
                        self.alien_hit_sound.play()
                        

                #alien extra hit
                self.extra_score = (500,300,250,200,100)
                if pygame.sprite.spritecollide(fire,self.extra,True):
                    self.score += choice(self.extra_score)
                    fire.kill()
                    self.alien_extra_hit_sound.play()

                
                     
                #alien laser hit
                if pygame.sprite.spritecollide(fire,self.alien_fire,True):
                  fire.kill()
        #alien fire          
        if self.alien_fire:
            for fire in self.alien_fire:
                  #obstacle hit
                if pygame.sprite.spritecollide(fire,self.blocks,True):
                  fire.kill()
                #player hit 
                if pygame.sprite.spritecollide(fire,self.player,False):
                    fire.kill()
                    self.lives -= 1
                    self.player_hit_sound.play()
                    if self.lives <= 0:
                        print("game over")
                        print(self.score)
                        pygame.quit()
                        sys.exit()
                #aliens hit
        if self.alien:
            for alien in self.alien:
                pygame.sprite.spritecollide(alien,self.blocks,True)
                if pygame.sprite.spritecollide(alien,self.player,False):
                    self.player_hit_sound.play()
                    print("game over")
                    print(self.score)
                    pygame.quit()
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_position + (live * self.live_surf.get_size()[0] + 10)
            screen.blit(self.live_surf,(x,8))
            
            
    def scores(self):
        score_surf = self.font.render(f'score:{self.score}',False,"white")
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)
        
    

    def win_game(self):
        if len(self.alien) == 0:
            self.dificult_speed += 1
            self.alien_setup(rows = 5, cols = 11)        

#   game draw                 
    def run(self):
        self.player.update()
        self.alien.update(self.alien.direct)
        self.alien_position_check()
        self.alien_fire.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collisions_event()
        self.display_lives()
        self.scores()
        self.win_game()

        self.player.sprite.firer.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)
        self.alien.draw(screen)
        self.alien_fire.draw(screen)
        self.extra.draw(screen)

# programção da janela, configurada com o tamanho altura, largura = 800x680
if __name__ == "__main__":
    pygame.init()
    size = width, height = 800, 680
    speed = [1, 10]
    screen = pygame.display.set_mode((width, height))
    pygame.time.Clock()
    clock = pygame.time.Clock()
    live = 3
    game = Game()

    ALIENFIRE = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENFIRE,1000)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENFIRE:
                game.alien_shoot()

        game.run()
        pygame.display.flip()
        screen.fill(("black"))
        clock.tick(60)

