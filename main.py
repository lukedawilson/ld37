import pygame, random, sys, math
from pygame.locals import *
from robot_algorithm import *
from robot import Sprite

input = """
fd
fd
sh
rr
fd
sh
sh
fd
rl
sh
rl
sh
"""

input2 = """
if el
    rl
    sh
    sh
    sh
    rr
end
if er
    rr
    sh
    sh
    sh
    rl
end
if ef
    sh
    sh
    sh
end
"""


def die(score = 0):
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




class GameEnvironment:
    def __init__(self):
        self.robots = []
        self.bullets = []
        self.enemies = []
    def clean_up_bullets_and_dead(self):
        self.mark_dead()
        self.clean_up_bullets()
        self.clean_up_enemies()
        self.clean_up_robots()
        if len(self.robots) == 0:
            die()
    def mark_dead(self):
        for i, bullet in enumerate(self.bullets):
            for j, enemy in enumerate(self.enemies):
                if (enemy.position[0] - 2 <= bullet.position[0] <= enemy.position[0] + 19) and \
                    (enemy.position[1] - 2 <= bullet.position[1] <= enemy.position[1] + 19):
                    self.bullets[i].dead = True
                    self.enemies[j].dead = True
        for j, enemy in enumerate(self.enemies):
            for k, robot in enumerate(self.robots):
                if (enemy.position[0] - 10 <= robot.position[0] <= enemy.position[0] + 10) and \
                    (enemy.position[1] - 10 <= robot.position[1] <= enemy.position[1] + 10):
                    self.robots[k].dead = True
    def clean_up_bullets(self):
        new_bullets = []
        for bullet in self.bullets:
            if (not bullet.hit_wall and not bullet.dead):
                new_bullets.append(bullet)
        self.bullets = new_bullets
    def clean_up_enemies(self):
        new_enemies = []
        for enemy in self.enemies:
            if not enemy.dead:
                new_enemies.append(enemy)
        self.enemies = new_enemies
    def clean_up_robots(self):
        new_robots = []
        for robot in self.robots:
            if not robot.dead:
                new_robots.append(robot)
        self.robots = new_robots
    def update_enemy_positions(self):
        robot_position = [0,0]
        for robot in self.robots:
            robot_position[0] += robot.position[0]
            robot_position[1] += robot.position[1]
        robot_position[0] /= len(self.robots)
        robot_position[1] /= len(self.robots)
        for i, enemy in enumerate(self.enemies):
            length = math.sqrt(((robot_position[0] - enemy.position[0]) ** 2) + ((robot_position[1] - enemy.position[1]) ** 2))
            enemy_to_robot = [float(robot_position[0] - enemy.position[0]) / length , float(robot_position[1] - enemy.position[1]) / length]
            self.enemies[i].position[0] += enemy_to_robot[0]
            self.enemies[i].position[1] += enemy_to_robot[1]
            if abs(enemy_to_robot[0]) > abs(enemy_to_robot[1]):
                if enemy_to_robot[0] > 0:
                    self.enemies[i].direction = 90
                else:
                    self.enemies[i].direction = 270
            else:
                if enemy_to_robot[1] > 0:
                    self.enemies[i].direction = 180
                else:
                    self.enemies[i].direction = 0

            self.enemies[i].animate_img()


def game_loop():



    run_game = True
    fps = 30
    game_environment = GameEnvironment()



    pygame.display.set_caption('Robotron')
    pygame.display.update()

    start_game()

    ## enemies converge to the average of the robots, better if they target the closest one so they dont all converge on each other
    ## algo only work for one robot
    ## manual movement only works for one robot

    robot = Sprite(game_environment, type='robot', x_position=50, y_position=200)
    game_environment.robots.append(robot)
    robot = Sprite(game_environment, type='robot', x_position=200, y_position=200)
    game_environment.robots.append(robot)
    robot = Sprite(game_environment, type='robot', x_position=500, y_position=50)
    game_environment.robots.append(robot)
    robot = Sprite(game_environment, type='robot', x_position=100, y_position=500)
    game_environment.robots.append(robot)

    algo = RobotAlgorithm(robot, input2)

    enemy = Sprite(game_environment, type='enemy', x_position=400, y_position=400)
    game_environment.enemies.append(enemy)
    enemy = Sprite(game_environment, type='enemy', x_position=200, y_position=100)
    game_environment.enemies.append(enemy)
    enemy = Sprite(game_environment, type='enemy', x_position=300, y_position=100)
    game_environment.enemies.append(enemy)
    enemy = Sprite(game_environment, type='enemy', x_position=500, y_position=200)
    game_environment.enemies.append(enemy)

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
                if e.key == K_p:
                    pause()
            elif e.type == KEYUP:
                if e.key == K_UP:
                    up_down -= 1
                elif e.key == K_DOWN:
                    up_down += 1

        rotate = 0

        algo.run_next_command()
        robot.rotate(rotate)
        robot.move_forward(up_down)

        game_environment.update_enemy_positions()

        s.fill(white)
        for bullet in game_environment.bullets:
            bullet.update_for_velocity()
            s.blit(bullet.img, bullet.position)
        for robot in game_environment.robots:
            s.blit(robot.img, robot.position)
        for enemy in game_environment.enemies:
            s.blit(enemy.img, enemy.position)

        game_environment.clean_up_bullets_and_dead()


        pygame.display.update()


    pygame.display.quit()
    quit()



game_intro()
game_loop()