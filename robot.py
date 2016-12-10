#TODO this is a stub of your Robot class - replace with import of real thing
import pygame

screen_w, screen_h = 800, 600
black = (0, 0, 0)
bullet_img = pygame.Surface((3, 3))
bullet_img.fill(black)

class Sprite:
    def __init__(self, game_environment, sprite_image, x_position=250, y_position=250, direction=0, velocity=0,
                 sprite_size=20):
        self.game_environment = game_environment
        self.position = [x_position, y_position]
        self.direction = direction
        self.move_size = 20
        self.img = sprite_image
        self.original_img = sprite_image
        self.velocity = velocity
        self.hit_wall = False
        self.dead = False
        self.sprite_size = sprite_size
    def rotate(self, angle):
        self.direction += angle
        self.direction = self.direction % 360
        self.img = pygame.transform.rotate(self.original_img, -self.direction)
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
    def shoot(self, velocity = 20):
        new_bullet = Sprite(self.game_environment, sprite_image=bullet_img, x_position=self.position[0] + 10,
                            y_position=self.position[1] + 10, direction=self.direction, velocity=velocity,
                            sprite_size=3)
        self.game_environment.bullets.append(new_bullet)
    def enemy_left(self):
        return False
    def enemy_right(self):
        return False
    def enemy_front(self):
        return False
    def wall_front(self):
        return False

