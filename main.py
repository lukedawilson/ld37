import pygame, random, sys
from pygame.locals import *

def die(score):
    message_to_screen('GAME OVER', red, y_displace=-75, size='large')
    message_to_screen('Your score was: '+str(score)+', press space to play again, q to quit', black)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            return
        elif event.type == KEYDOWN:
            if event.key == K_q:
                return
            elif event.key == K_SPACE:
                game_loop()

def start_game():
    s.fill(white)
    message_to_screen('Press space to start', black)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.display.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                return
def pause():
    message_to_screen('Paused', black, size='large')
    message_to_screen('Press space or p to start', black, y_displace=100)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.display.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                return
            elif event.key == K_p:
                return
        clock.tick(5)

def game_intro():
    s.fill(white)
    message_to_screen('Welcome to', green, -170, 'medium')
    message_to_screen('Robotron', green, -100, 'large')
    message_to_screen('Kill enemy robots', black)
    message_to_screen('Press space to play again, q to quit', black, 150)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    quit()
                elif event.key == K_SPACE:
                    return

        clock.tick(5)

def message_to_screen(msg, colour, y_displace=0, size='small'):
    if size == 'small':
        text_surf = smallfont.render(msg, True, colour)
    elif size == 'medium':
        text_surf = medfont.render(msg, True, colour)
    elif size == 'large':
        text_surf = largefont.render(msg, True, colour)
    text_rect = text_surf.get_rect()
    text_rect.center = (screen_w / 2, (screen_h / 2) + y_displace)
    s.blit(text_surf, text_rect)
    pygame.display.update()



black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
grey = (100, 100, 100)
screen_w, screen_h = 800, 600

pygame.init()
s = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 80)



img = pygame.Surface((20, 20))
img.fill(white)
pygame.draw.polygon(img, grey, ((5, 20), (10, 0), (15, 20)))

bullet_img = pygame.Surface((3, 3))
bullet_img.fill(black)



## skier_c = pygame.image.load('skier_c.png')


class Sprite:
    def __init__(self, game_environment, x_position=250, y_position=250, direction=0, velocity=0, sprite_image = img):
        self.game_environment = game_environment
        self.position = [x_position, y_position]
        self.direction = direction
        self.move_size = 20
        self.img = sprite_image
        self.velocity = velocity
        #self.s = s
    def rotate(self, angle):
        self.direction += angle
        self.direction = self.direction % 360
        self.img = pygame.transform.rotate(img, -self.direction)
    def move_forward(self, up_down=1):
        self.move_forward_by(up_down * self.move_size)
    def move_forward_by(self, move_distance):
        if self.direction == 0:
            self.position[1] -= move_distance
        elif self.direction == 90:
            self.position[0] += move_distance
        elif self.direction == 180:
            self.position[1] += move_distance
        elif self.direction == 270:
            self.position[0] -= move_distance
        self.position[0] = max(0, min(screen_w - 20, self.position[0]))
        self.position[1] = max(0, min(screen_h - 20, self.position[1]))
    def update_for_velocity(self):
        self.move_forward_by(self.velocity)
    def shoot(self, velocity = 20):
        new_bullet = Sprite(self.game_environment, x_position=self.position[0] + 10, y_position=self.position[1] + 10, direction=self.direction, velocity=velocity, sprite_image = bullet_img)
        self.game_environment.bullets.append(new_bullet)


class GameEnvironment:
    def __init__(self):
        self.sprites = []
        self.bullets = []

def game_loop():



    run_game = True
    fps = 30
    game_environment = GameEnvironment()



    pygame.display.set_caption('Robotron')
    pygame.display.update()

    start_game()

    robot = Sprite(game_environment)
    game_environment.sprites = [robot]

    up_down = 0 # = 1 if up is pressed, -1 if down is pressed, 0 if neither or both


    while run_game:
        clock.tick(fps)

        for e in pygame.event.get():
            if e.type == QUIT:
                run_game = False
            elif e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    robot.rotate(90)
                elif e.key == K_LEFT:
                    robot.rotate(-90)
                elif e.key == K_UP:
                    up_down += 1
                elif e.key == K_DOWN:
                    up_down -= 1
                elif e.key == K_SPACE:
                    robot.shoot()
                elif e.key == K_p:
                    pause()
            elif e.type == KEYUP:
                if e.key == K_UP:
                    up_down -= 1
                elif e.key == K_DOWN:
                    up_down += 1

        rotate = 0

        robot.rotate(rotate)
        robot.move_forward(up_down)



        s.fill(white)
        for bullet in game_environment.bullets:
            bullet.update_for_velocity()
            s.blit(bullet.img, bullet.position)
        for sprite in game_environment.sprites:
            s.blit(sprite.img, sprite.position)


        pygame.display.update()


    pygame.display.quit()
    quit()



game_intro()
game_loop()