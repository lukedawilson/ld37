from time import sleep
from robot_algorithm import RobotAlgorithm

class Sprite:
    def rotate(self, angle):
        print 'Rotate ' + str(angle) + ' degrees'
        
    def move_forward(self, direction=1): # 1=forward, -1=backwards, 0=sit on yer arse
        print 'Move ' + ('forwards' if 1 else ('backwards' if -1 else 'nowhere'))
        
    def shoot(self, velocity=10):
        print 'Shoot at ' + str(velocity) + ' velocity'
        
    def enemy_left(self):
        return False
        
    def enemy_right(self):
        return False
        
    def enemy_front(self):
        return False
        
    def wall_front(self):
        return False
        
    def dead(self):
        return False

input = """
if el
    rl
    if ef
        sh
    end
    fd
end
if er
    rr
    sh
end
if ef
    sh
end
fd
sh
"""

robot = Sprite()
algo = RobotAlgorithm(robot, input)

for _ in range(20):
    algo.run_next_command()
    sleep(0.3)
    