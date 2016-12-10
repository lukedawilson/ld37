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


## skier_c = pygame.image.load('skier_c.png')



def game_loop():



    run_game = True
    fps = 30




    pygame.display.set_caption('Robotron')
    pygame.display.update()

    start_game()

    rotate, forward = 0, 0
    move_size = 20
    position = [250, 250]
    direction = 0


    while run_game:
        clock.tick(fps)

        for e in pygame.event.get():
            if e.type == QUIT:
                run_game = False
            elif e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    rotate += 90
                elif e.key == K_LEFT:
                    rotate -= 90
                elif e.key == K_UP:
                    forward += move_size
                elif e.key == K_DOWN:
                    forward -= move_size
                elif e.key == K_p:
                    pause()
            elif e.type == KEYUP:
                if e.key == K_UP:
                    forward -= move_size
                elif e.key == K_DOWN:
                    forward += move_size

        direction -= rotate
        rotate = 0
        direction = direction % 360
        if direction == 0:
            position[1] -= forward
        elif direction == 90:
            position[0] -= forward
        elif direction == 180:
            position[1] += forward
        elif direction == 270:
            position[0] += forward

        s.fill(white)
        #message_to_screen('position, forward, rotate, direction' + str(position[0]) + '-' + str(position[1]) + ', ' + str(forward) + ', ' + str(rotate) + ' ' + str(direction), green, -170, 'small')
        robot = pygame.transform.rotate(img, direction)
        s.blit(robot, position)


        pygame.display.update()


    pygame.display.quit()
    quit()



game_intro()
game_loop()