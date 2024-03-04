import pygame

port = 8081
host = '127.0.0.1'
byte_limit = 8192
WIDTH, HEIGHT = 900, 600
bullet_image = pygame.Surface((5,5))
bullet_image.fill('white')

class Bullet:
    def __init__(self, player_pos, id, direction):
        self.direction = direction
        self.rect = bullet_image.get_rect(center=player_pos)
        self.can_shoot = True
        self.id = id
        if int(self.id) % 2 == 0:
            # self.rect.x -= speed
            self.team = True
        else:
            # self.rect.x += speed
            self.team = False

    def update(self):
        speed = 10
        self.rect.center += self.direction * speed
        
        