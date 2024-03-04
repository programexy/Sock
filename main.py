from network import Network
from pickle import dumps, loads
import pygame
import sys
from settings import *
# import asyncio

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font(None, 20)


class Player:
    def __init__(self):
        if int(network.id)%2 == 0:
            self.pos = pygame.math.Vector2(WIDTH - 36, HEIGHT // 2)
            self.team = True
        else:
            print(network.id)
            self.pos = pygame.math.Vector2(36, HEIGHT // 2)

            self.team = False

        self.direction = pygame.math.Vector2()
        self.speed = 10
        self.reload_time = pygame.time.get_ticks()


    def input(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        global bullet, bullet_direction
        if keys[pygame.K_UP]:
            self.direction.y = -1
            # bullet_direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            # bullet_direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            # bullet_direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            # bullet_direction.x = 1
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and current_time - self.reload_time >= 200:
            bullets.append(Bullet(self.pos, network.id, self.direction))
            # print(current_time, self.reload_time)
            self.reload_time = current_time

    def update(self):
        self.pos += self.direction * self.speed
        self.input()


def draw(name):
    global rect, image
    if name == network.id:
        image.fill('red')
    else:
        image.fill('blue')
    screen.blit(image, rect)


# Basic parameters of the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
# Used to adjust the frame rate
clock = pygame.time.Clock()
FPS = 60
network = Network()
bullet_direction = pygame.math.Vector2(0, 1)
self_player = Player()
bullets = []
image = pygame.Surface((20,20))
rect = image.get_rect(center=self_player.pos)


def main():
    global rect, image
    while True:
        screen.fill('black')

        network.send(
            {'id': network.id, 'name': network.name, 'position': self_player.pos, 'rect': rect, 'bullets': bullets}
        )
        self_player.update()
        for BULLET in bullets:
            BULLET.update()

            print(BULLET.rect.center)
            if BULLET.rect.centerx > WIDTH or BULLET.rect.centerx < 0:
                bullets.remove(BULLET)
            screen.blit(bullet_image, BULLET.rect)

        player_data = network.receive()

        for player_id in player_data.keys():
            rect = image.get_rect(center=player_data[player_id]['position'])
            draw(player_id)
            # screen.blit(bullet_image, player_data[player_id]['bullet_rect'])
            # player_data[player_id]['position'],
            # print(player_data[player_name], player_name)
            for all_bullet in player_data[player_id]['bullets']:
                screen.blit(bullet_image, all_bullet.rect)

                if all_bullet.rect.colliderect(rect) and network.id != player_id:
                    print('Ouch')


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Disconnecting!')
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(FPS)


main()
