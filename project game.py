import sys
import random
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('C:/Users/DELL/Documents/pygame/cyberfunk.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1) 


player_ship = 'C:/Users/DELL/Documents/pygame/plyship.png'
enemy_ship = 'C:/Users/DELL/Documents/pygame/enemyship.png'
ufo_ship = 'C:/Users/DELL/Documents/pygame/ufo.png'

screen = pygame.display.set_mode((800,600))
s_width, s_height = 800, 600

clock = pygame.time.Clock()
FPS = 60

background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((3,3))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, s_width)
        self.rect .y = random.randrange(0, s_height)

    def update(self):
        self.rect.y += 2
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(0, s_width)

class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        try:
            self.image = pygame.image.load(img).convert_alpha()
        except:
            self.image = pygame.Surface((50,50))
            self.image.fill('red')

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shoot(self):
        bullet = PlayerBullet()
        bullet.rect.centerx = self.rect.centerx
        bullet.rect.bottom = self.rect.top
        playerbullet_group.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        try:
            self.image = pygame.image.load(img).convert_alpha()
        except:
            self.image = pygame.Surface((40,40))
            self.image.fill('blue')

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(-1000, 0)
        self.hp = 3

    def update(self):
        self.rect.y += 2
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-1000, 0)
            self.hp = 3 

class Ufo(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        try:
            self.image = pygame.image.load(img).convert_alpha()
        except:
            self.image = pygame.Surface((60,40))
            self.image.fill('green')

        self.rect = self.image.get_rect()
        self.rect.x = -200
        self.rect.y = 200
        self.move = 3
        self.hp = 5

    def update(self):
        self.rect.x += self.move
        if self.rect.x > s_width + 200 or self.rect.x < -200:
            self.move *= -1

class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 15
        if self.rect.y < 0:
            self.kill()

class Game:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont(None, 40)

        self.create_background()
        self.create_player()
        self.create_enemy()
        self.create_ufo()
        self.run()

    def create_background(self):
        for i in range(100):
            background_group.add(Background())

    def create_player(self):
        self.player = Player(player_ship)
        player_group.add(self.player)

    def create_enemy(self):
        for i in range(5):
            enemy_group.add(Enemy(enemy_ship))

    def create_ufo(self):
        ufo_group.add(Ufo(ufo_ship))

    def hit_enemy(self):
        hits = pygame.sprite.groupcollide(enemy_group, playerbullet_group, False, True)

        for enemy in hits:
            enemy.hp -= 1

            if enemy.hp <= 0:
                self.score += 10
                enemy.rect.x = random.randrange(0, s_width)
                enemy.rect.y = random.randrange(-1000, 0)
                enemy.hp = 3

    def hit_ufo(self):
        hits = pygame.sprite.groupcollide(ufo_group, playerbullet_group, False, True)

        for ufo in hits:
            ufo.hp -= 1

            if ufo.hp <= 0:
                self.score += 50
                ufo.rect.x = -200
                ufo.hp = 5
              
    def hit_player(self):
        
        hits = pygame.sprite.spritecollide(self.player, enemy_group, False)
        if hits:
            self.lives -= 1
        for enemy in hits:
            enemy.rect.x = random.randrange(0, s_width)
            enemy.rect.y = random.randrange(-1000, 0)

        hits = pygame.sprite.spritecollide(self.player, ufo_group, False)
        if hits:
            self.lives -= 1
            for ufo in hits:
                ufo.rect.x = -200            

    def run(self):
        while True:
            screen.fill('black')

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == K_SPACE:
                        self.player.shoot()

            background_group.update()
            enemy_group.update()
            ufo_group.update()
            playerbullet_group.update()
            player_group.update()

            self.hit_enemy()
            self.hit_ufo()
            self.hit_player()

            background_group.draw(screen)
            enemy_group.draw(screen)
            ufo_group.draw(screen)
            playerbullet_group.draw(screen)
            player_group.draw(screen)

            score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
            screen.blit(score_text, (10, 10))
            lives_text = self.font.render(f"Lives: {self.lives}", True, (255,255,255))
            screen.blit(lives_text, (10, 50))
            
            if self.lives <= 0:
                game_over_text = self.font.render("GAME OVER", True, (255,0,0))
                screen.blit(game_over_text, (s_width//2 - 100, s_height//2))
                pygame.display.update()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()

            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    Game()