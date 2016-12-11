import pygame, random, sys, math
from pygame.locals import *
from robot_algorithm import *
from robot import Sprite
from time import sleep

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
# if el
#     rl
#     sh
#     sh
#     sh
#     fd
#     rr
# end
# if er
#     rr
#     sh
#     sh
#     sh
#     fd
#     rl
# end

input2 = """
if ef
    sh 3
end
if er
    tr
    sh 3
    tl
end
if el
    tl
    sh 3
    tr
end
if ff
    sh 3
end
fd
rr


"""


def die(score = 0):
    message_to_screen('GAME OVER', red, y_displace=-75, size='large')
    message_to_screen('Your score was: '+str(score)+', press return to play again, q to quit', red)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.display.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_q:
                pygame.display.quit()
                quit()
            elif event.key == K_RETURN:
                return

def level_complete():
    message_to_screen('Level complete', red, y_displace=-75, size='large')
    sleep(3)

def start_game():
    s.fill(white)
    message_to_screen('Press return to start', black)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.display.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
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
    message_to_screen('Progotron', green, -100, 'large')
    message_to_screen('Kill enemy robots', black)
    message_to_screen('Press return to play again, q to quit', black, 150)
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
                elif event.key == K_RETURN:
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
number_of_robots = 4

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








class GameEnvironment:
    def __init__(self):
        self.robots = []
        self.bullets = []
        self.enemies = []
        self.algos = []


    def run_next_algo_command(self):
        for algo in self.algos:
            algo.run_next_command()
    def clean_up_bullets_and_dead(self):
        self.mark_dead()
        self.clean_up_bullets()
        self.clean_up_enemies()
        self.clean_up_robots()
        if len(self.robots) == 0:
            die()
            return 'die', len(self.robots)
        if len(self.enemies) == 0:
            level_complete()
            return 'success', len(self.robots)
        else:
            return 'continue', len(self.robots)
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
        new_algos = []
        for i, robot in enumerate(self.robots):
            if not robot.dead:
                new_robots.append(robot)
                new_algos.append(self.algos[i])
        self.robots = new_robots
        self.algos = new_algos
    def update_enemy_positions(self):

        for enemy in self.enemies:
            nearest_robot = 0
            shortest_distance = 10000
            for i, robot in enumerate(self.robots):
                distance, _ = Sprite.polar(robot.position[0] - enemy.position[0], robot.position[1] - enemy.position[1])
                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_robot = i
            enemy_to_robot = [float(self.robots[nearest_robot].position[0] - enemy.position[0]) / shortest_distance ,
                              float(self.robots[nearest_robot].position[1] - enemy.position[1]) / shortest_distance]
            enemy.position[0] += enemy_to_robot[0]
            enemy.position[1] += enemy_to_robot[1]
            if abs(enemy_to_robot[0]) > abs(enemy_to_robot[1]):
                if enemy_to_robot[0] > 0:
                    enemy.direction = 90
                else:
                    enemy.direction = 270
            else:
                if enemy_to_robot[1] > 0:
                    enemy.direction = 180
                else:
                    enemy.direction = 0

            enemy.animate_img()


def game():
    while True:
        game_intro()
        level = 1
        no_of_robots = 4
        level_outcome = 'success'
        while level_outcome == 'success':
            level_outcome, no_of_robots = game_level(level, no_of_robots)
            level += 1

def game_level(level, no_of_robots):



    run_game = True
    fps = 30
    game_environment = GameEnvironment()



    pygame.display.set_caption('Progrotron')
    pygame.display.update()

    start_game()

    ## add in level display and robot display
    ## make a robotron style level complete
    ## starting screen

    for i in range(no_of_robots):
        rand_x = random.random()
        rand_y = random.random()
        x_start_position = 0.6 * rand_x * screen_w + 0.2 * screen_w
        y_start_position = 0.6 * rand_y * screen_h + 0.2 * screen_h
        robot = Sprite(game_environment, type='robot', x_position=x_start_position, y_position=y_start_position)
        game_environment.robots.append(robot)
        algo = RobotAlgorithm(robot, input2)
        game_environment.algos.append(algo)





    for i in range(level + 5):
        rand_x = random.random()
        rand_y = random.random()
        x_start_position = rand_x * (screen_w - 20)
        y_start_position = rand_y * (screen_h - 20)
        enemy = Sprite(game_environment, type='enemy', x_position=x_start_position, y_position=y_start_position)
        game_environment.enemies.append(enemy)


    up_down = 0 # = 1 if up is pressed, -1 if down is pressed, 0 if neither or both
    shoot = False


    while run_game:
        clock.tick(fps)

        rotate = 0
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.display.quit()
                quit()
            elif e.type == KEYDOWN:
                if e.key == K_RIGHT:
                    rotate = 90
                elif e.key == K_LEFT:
                    rotate = -90
                elif e.key == K_UP:
                    up_down += 1
                elif e.key == K_DOWN:
                    up_down -= 1
                elif e.key == K_SPACE:
                    shoot = True
                if e.key == K_p:
                    pause()
            elif e.type == KEYUP:
                if e.key == K_UP:
                    up_down -= 1
                elif e.key == K_DOWN:
                    up_down += 1


        game_environment.run_next_algo_command()
        for robot in game_environment.robots:
            robot.rotate(rotate)
            robot.move_forward(up_down)
            if shoot:
                robot.shoot()

        shoot = False

        game_environment.update_enemy_positions()

        s.fill(black)
        for bullet in game_environment.bullets:
            bullet.update_for_velocity()
            s.blit(bullet.img, bullet.position)
        for robot in game_environment.robots:
            s.blit(robot.img, robot.position)
        for enemy in game_environment.enemies:
            s.blit(enemy.img, enemy.position)

        level_outcome, no_of_robots = game_environment.clean_up_bullets_and_dead()


        pygame.display.update()

        if level_outcome == 'die' or level_outcome == 'success':
            run_game = False


    return level_outcome, no_of_robots


game()
