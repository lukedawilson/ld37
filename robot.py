#TODO this is a stub of your Robot class - replace with import of real thing
import pygame
import math



screen_w, screen_h = 800, 600
black = (0, 0, 0)
white = (255, 255, 255)
bullet_img = pygame.Surface((3, 3))
bullet_img.fill(white)

images = {'robot': {0:{}, 90:{}, 180:{}, 270:{}}, 'enemy': {0:{}, 90:{}, 180:{}, 270:{}}}

images['robot'][180][0] = pygame.image.load('sprites/robot1.png')
images['robot'][180][1] = pygame.image.load('sprites/robot2.png')
images['robot'][180][2] = pygame.image.load('sprites/robot1.png')
images['robot'][180][3] = pygame.image.load('sprites/robot3.png')
images['robot'][0][0] = pygame.image.load('sprites/robot_back1.png')
images['robot'][0][1] = pygame.image.load('sprites/robot_back2.png')
images['robot'][0][2] = pygame.image.load('sprites/robot_back1.png')
images['robot'][0][3] = pygame.image.load('sprites/robot_back3.png')
images['robot'][270][0] = pygame.image.load('sprites/robot_left.png')
images['robot'][270][1] = pygame.image.load('sprites/robot_left.png')
images['robot'][270][2] = pygame.image.load('sprites/robot_left2.png')
images['robot'][270][3] = pygame.image.load('sprites/robot_left2.png')
images['robot'][90][0] = pygame.image.load('sprites/robot_right.png')
images['robot'][90][1] = pygame.image.load('sprites/robot_right.png')
images['robot'][90][2] = pygame.image.load('sprites/robot_right2.png')
images['robot'][90][3] = pygame.image.load('sprites/robot_right2.png')

images['enemy'][180][0] = pygame.image.load('sprites/enemy1.png')
images['enemy'][180][1] = pygame.image.load('sprites/enemy2.png')
images['enemy'][180][2] = pygame.image.load('sprites/enemy1.png')
images['enemy'][180][3] = pygame.image.load('sprites/enemy3.png')
images['enemy'][0][0] = pygame.image.load('sprites/enemy_back1.png')
images['enemy'][0][1] = pygame.image.load('sprites/enemy_back2.png')
images['enemy'][0][2] = pygame.image.load('sprites/enemy_back1.png')
images['enemy'][0][3] = pygame.image.load('sprites/enemy_back3.png')
images['enemy'][270][0] = pygame.image.load('sprites/enemy_left.png')
images['enemy'][270][1] = pygame.image.load('sprites/enemy_left.png')
images['enemy'][270][2] = pygame.image.load('sprites/enemy_left2.png')
images['enemy'][270][3] = pygame.image.load('sprites/enemy_left2.png')
images['enemy'][90][0] = pygame.image.load('sprites/enemy_right.png')
images['enemy'][90][1] = pygame.image.load('sprites/enemy_right.png')
images['enemy'][90][2] = pygame.image.load('sprites/enemy_right2.png')
images['enemy'][90][3] = pygame.image.load('sprites/enemy_right2.png')



class Sprite:
    def __init__(self, game_environment, x_position=250, y_position=250, direction=180, velocity=0,
                 sprite_size=20, type='robot'):
        self.game_environment = game_environment
        self.position = [x_position, y_position]
        self.direction = direction
        self.move_size = 20
        if type=='robot' or type=='enemy':
            self.img = images[type][self.direction][0]
        elif type=='bullet':
            self.img = bullet_img
        self.velocity = velocity
        self.hit_wall = False
        self.dead = False
        self.sprite_size = sprite_size
        self.type = type
        self.animation = 0
        self.animation_pause = 0
        self.enemy_near_length = 20
        self.enemy_near_angle = 15
    def animate_img(self):
        if self.animation_pause == 0:
            self.animation += 1
            if self.animation == 4:
                self.animation = 0
            self.img = images[self.type][self.direction][self.animation]
            self.animation_pause = 1
        else:
            self.animation_pause = 0
    def rotate(self, angle):
        self.direction += angle
        self.direction = self.direction % 360
        if self.direction == 0:
            self.img = images[self.type][self.direction][self.animation]
        elif self.direction == 90:
            self.img = images[self.type][self.direction][self.animation]
        elif self.direction == 180:
            self.img = images[self.type][self.direction][self.animation]
        elif self.direction == 270:
            self.img = images[self.type][self.direction][self.animation]

        #self.img = pygame.transform.rotate(self.original_img, -self.direction)
    def move_forward(self, up_down=1):
        self.move_forward_by(up_down * self.move_size)
        self.animate_img()


    def move_forward_by(self, move_distance):
        if self.direction == 0:
            self.position[1] -= move_distance
        elif self.direction == 90:
            self.position[0] += move_distance
        elif self.direction == 180:
            self.position[1] += move_distance
        elif self.direction == 270:
            self.position[0] -= move_distance
        self.check_for_walls()
    def check_for_walls(self):
        if (self.position[0] < 0) or (self.position[0] > screen_w - self.sprite_size):
            self.position[0] = max(0, min(screen_w - self.sprite_size, self.position[0]))
            self.hit_wall = True
        if (self.position[1] < 0) or (self.position[1] > screen_h - self.sprite_size):
            self.position[1] = max(0, min(screen_h - self.sprite_size, self.position[1]))
            self.hit_wall = True
    def update_for_velocity(self):
        self.move_forward_by(self.velocity)
    def shoot(self, velocity = 30):
        new_bullet = Sprite(self.game_environment, x_position=self.position[0] + 10,
                            y_position=self.position[1] + 10, direction=self.direction, velocity=velocity,
                            sprite_size=3, type='bullet')
        self.game_environment.bullets.append(new_bullet)
    def enemy_left(self):
        direction_looking = self.direction - 90
        direction_looking = direction_looking % 360
        return self.enemy_near(direction_looking)

    def enemy_right(self):
        direction_looking = self.direction + 90
        direction_looking = direction_looking % 360
        return self.enemy_near(direction_looking)
    def enemy_front(self):
        direction_looking = self.direction
        direction_looking = direction_looking % 360
        return self.enemy_near(direction_looking)
    def enemy_near(self, direction_looking):
        for enemy in self.game_environment.enemies:
            polar_coords = Sprite.polar(enemy.position[0] - self.position[0] , - enemy.position[1] + self.position[1])
            # print polar_coords, direction_looking
            if polar_coords[0] < (self.enemy_near_length * self.sprite_size) and \
                abs(polar_coords[1] - direction_looking) < self.enemy_near_angle:
                return True
        return False

    @staticmethod
    def polar(x, y):
        return math.hypot(x,y), math.degrees(math.atan2(x, y)) % 360

    def wall_front(self):
        if self.direction == 0 and self.position[1] < self.sprite_size:
            return True
        elif self.direction == 90 and self.position[0] > screen_w - self.sprite_size - self.sprite_size:
            return True
        elif self.direction == 270 and self.position[0] < self.sprite_size:
            return True
        elif self.direction == 180 and self.position[1] > screen_h - self.sprite_size - self.sprite_size:
            return True
        else:
            return False


