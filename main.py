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
    rr
    sh 3
    rl
end
if el
    rl
    sh 3
    rr
end
if ff
    sh 3
end
fd
rr


"""

input3 = """
if ef
    sh 3
else
    if el
        rl
        sh 3
    else
        if er
            rr
            sh 3
        else
            if wf
                rr 2
                fd 3
            else
                if ff
                    rl
                    fd 2
                else
                    fd 3
                end
            end
        end
    end
end
"""


def die(level):
    message_to_screen('GAME OVER', red, y_displace=-75, size='large')
    message_to_screen('level reached: '+str(level)+', press return to play again, q to quit', red)
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
    s.fill(black)
    message_to_screen('Press return to start', yellow)
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.display.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                return
def pause():
    message_to_screen('Paused', yellow, size='large')
    message_to_screen('Press space or p to start', yellow, y_displace=100)
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
    s.fill(black)
    s.blit(title_img, [130, 100])
    s.blit(subtitle_img, [315, 170])
    message_to_screen('Created by', yellow)
    message_to_screen('Luke Wilson, Nathan Varughese and Matthew Varughese', yellow, 30)
    message_to_screen('Program your robots to shoot down the enemy robots', yellow, 200)
    message_to_screen('Press return to play, q to quit', blue, 250)
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

def print_settings_screen(robots, enemies, enemy_inc, manual_control, friendly_fire):
    s.fill(black)
    message_to_screen('Settings, escape to continue', blue, -250, update=False)
    message_to_screen('Robots (press q, w): ' + str(robots), yellow, -50, update=False)
    message_to_screen('Enemies (press a, s): ' + str(enemies), yellow, 0, update=False)
    message_to_screen('Enemy increase per level (press z, x): ' + str(enemy_inc), yellow, 50, update=False)
    message_to_screen('Manually control robots(press m): ' + str(manual_control), yellow, 100, update=False)
    message_to_screen('Friendly fire kills(press f): ' + str(friendly_fire), yellow, 150, update=False)
    pygame.display.update()

def setting_screen(robots, enemies, enemy_inc, manual_control, friendly_fire):

    print_settings_screen(robots, enemies, enemy_inc, manual_control, friendly_fire)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    robots -= 1
                    robots = max(1, robots)
                elif event.key == K_w:
                    robots += 1
                elif event.key == K_a:
                    enemies -= 1
                    enemies = max(1, enemies)
                elif event.key == K_s:
                    enemies += 1
                elif event.key == K_z:
                    enemy_inc -= 1
                    enemy_inc = max(0, enemy_inc)
                elif event.key == K_x:
                    enemy_inc +=1
                elif event.key == K_m:
                    manual_control = not manual_control
                elif event.key == K_f:
                    friendly_fire = not friendly_fire
                elif event.key == K_ESCAPE:
                    return robots, enemies, enemy_inc, manual_control, friendly_fire

                print_settings_screen(robots, enemies, enemy_inc, manual_control, friendly_fire)

        clock.tick(5)




def print_input_screen(text, cursor_pos):
    s.fill(black)
    message_to_screen('Input command, press escape when done', yellow, -250, update=False)
    box_width, box_height = 400, 400
    box_left, box_right = screen_w/2 - box_width/2, screen_w/2 + box_width/2
    box_top, box_bottom = screen_h/2 - box_height/2, screen_h/2 + box_height/2
    box_thickness = 2

    new_text = text[:cursor_pos] + '_' + text[cursor_pos:]
    lines = new_text.split('\n')
    for i, line in enumerate(lines):
        if '_' in line:
            message_to_screen(line.split('_')[0] + line.split('_')[1], white, i * 30, buffer_top=box_top + 5, buffer_left=box_left + 10, align='left', update=False)
            message_to_screen(line.split('_')[0] + '_', white, i * 30, buffer_top=box_top + 5, buffer_left=box_left + 10, align='left', update=False)
        else:
            message_to_screen(line, white, i * 30, buffer_top=box_top + 5, buffer_left=box_left + 10, align='left', update=False)
    pygame.draw.line(s, white, (box_left, box_top), (box_right, box_top), box_thickness)
    pygame.draw.line(s, white, (box_right, box_top), (box_right, box_bottom), box_thickness)
    pygame.draw.line(s, white, (box_right, box_bottom), (box_left, box_bottom), box_thickness)
    pygame.draw.line(s, white, (box_left, box_bottom), (box_left, box_top), box_thickness)

    pygame.display.update()

def program_input():

    cursor_pos = 0
    text = ''
    print_input_screen(text, cursor_pos)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    text = text[:cursor_pos] + '\n' + tabs(text[:cursor_pos]) * '    ' + text[cursor_pos:]
                    cursor_pos += tabs(text) * 4 + 1
                elif event.key == K_BACKSPACE:
                    if cursor_pos > 0:
                        text = text[:cursor_pos-1] + text[cursor_pos:]
                        cursor_pos -= 1
                elif event.key == K_TAB:
                    text = text[:cursor_pos] + '    ' + text[cursor_pos:]
                    cursor_pos += 4
                elif event.key == K_LEFT:
                    cursor_pos -= 1
                elif event.key == K_RIGHT:
                    cursor_pos += 1
                elif event.key == K_ESCAPE:
                    return text
                elif event.key < 127:
                    text = text[:cursor_pos] + (chr(event.key)) + text[cursor_pos:]
                    cursor_pos += 1

                cursor_pos = max(0, min(cursor_pos, len(text)))
                print_input_screen(text, cursor_pos)

        clock.tick(5)

def tabs(text):
    tabs = 0
    lines = text.split('\n')
    for line in lines:
        words = line.split(' ')
        for word in words:
            if word == 'if':
                tabs += 1
            elif word == 'end':
                tabs -= 1
    return max(0, tabs)

def message_to_screen(msg, colour, y_displace=0, size='small', buffer_left=0, buffer_top=0, align='centre', update=True):
    msg = msg.upper()
    if size == 'small':
        text_surf = smallfont.render(msg, True, colour)
    elif size == 'medium':
        text_surf = medfont.render(msg, True, colour)
    elif size == 'large':
        text_surf = largefont.render(msg, True, colour)

    if align != 'centre':
        s.blit(text_surf, (buffer_left, buffer_top + y_displace))
    else:
        text_rect = text_surf.get_rect()
        text_rect.center = (screen_w / 2, (screen_h / 2) + y_displace)
        s.blit(text_surf, text_rect)
    if update:
        pygame.display.update()



black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 155, 0)
grey = (100, 100, 100)
yellow = (250, 250, 0)
screen_w, screen_h = 800, 600
top_bottom_buffer, side_buffer, border_thickness = 50, 5, 3

pygame.init()
s = pygame.display.set_mode((screen_w, screen_h))
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont('consolas', 25)
medfont = pygame.font.SysFont('consolas', 50)
largefont = pygame.font.SysFont('consolas', 80)


title_img = pygame.image.load('progrotron_title.png')
subtitle_img = pygame.image.load('2084.png')

img = pygame.Surface((20, 20))
img.fill(white)
pygame.draw.polygon(img, grey, ((5, 20), (10, 0), (15, 20)))



bullet_img = pygame.Surface((3, 3))
bullet_img.fill(black)








class GameEnvironment:
    def __init__(self, level):
        self.robots = []
        self.bullets = []
        self.enemies = []
        self.algos = []
        self.level = level


    def run_next_algo_command(self):
        for algo in self.algos:
            algo.run_next_command()
    def clean_up_bullets_and_dead(self):
        self.mark_dead()
        self.clean_up_bullets()
        self.clean_up_enemies()
        self.clean_up_robots()
        if len(self.robots) == 0:
            die(self.level)
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
        robots, enemies, enemy_inc, manual_control, friendly_fire = setting_screen(4, 8, 2, False, False)
        text = program_input()
        level = 1
        no_of_robots = 4
        level_outcome = 'success'
        while level_outcome == 'success':
            level_outcome, no_of_robots = game_level(level, text, robots, enemies, enemy_inc, manual_control, friendly_fire)
            level += 1

def game_level(level, text, no_of_robots, no_of_enemies, enemy_inc, manual_control, friendly_fire):



    run_game = True
    fps = 30
    game_environment = GameEnvironment(level)



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
        algo = RobotAlgorithm(robot, text)
        game_environment.algos.append(algo)





    for i in range(no_of_enemies + (level - 1) * enemy_inc):
        rand_x = random.random()
        rand_y = random.random()
        x_start_position = rand_x * (screen_w - 20 - side_buffer * 2) + side_buffer
        y_start_position = rand_y * (screen_h - 20 - top_bottom_buffer * 2) + top_bottom_buffer
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
        pygame.draw.line(s, yellow, (side_buffer, top_bottom_buffer), (screen_w - side_buffer, top_bottom_buffer), border_thickness)
        pygame.draw.line(s, yellow, (screen_w - side_buffer, top_bottom_buffer), (screen_w - side_buffer, screen_h - top_bottom_buffer), border_thickness)
        pygame.draw.line(s, yellow, (screen_w - side_buffer, screen_h - top_bottom_buffer), (side_buffer, screen_h - top_bottom_buffer), border_thickness)
        pygame.draw.line(s, yellow, (side_buffer, screen_h - top_bottom_buffer), (side_buffer, top_bottom_buffer), border_thickness)
        message_to_screen(str(no_of_robots) + ' robots', red, -screen_h / 2 + top_bottom_buffer / 2, update=False)
        message_to_screen(str(level) + ' wave', red, screen_h / 2 - top_bottom_buffer / 2, update=False)
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
