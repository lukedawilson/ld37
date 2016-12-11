from robot_algorithm import RobotAlgorithm

class Sprite:
    def __init__(self, left = False, right = False, front = False):
        self.left = left
        self.right = right
        self.front = front
        self.commands = []
        
    def get_commands(self):
        return self.commands    

    def rotate(self, angle):
        self.commands.append('r ' + str(angle))
        
    def move_forward(self, direction=1): # 1=forward, -1=backwards, 0=sit on yer arse
        self.commands.append('mv ' + str(direction))
        
    def shoot(self, velocity=10):
        self.commands.append('sh ' + str(velocity))
        
    def enemy_left(self):
        return self.left
        
    def enemy_right(self):
        return self.right
        
    def enemy_front(self):
        return self.front

def test_basic_commands():
    input = """
    rl
    rr
    fd
    sh
    """
    robot = Sprite()
    algo = RobotAlgorithm(robot, input)

    for _ in range(4):    
        algo.run_next_command()
    
    print robot.get_commands() == ['r -90', 'r 90', 'mv 1', 'sh 15']
    
def test_repeat_arg():
    input = """
    rl 3
    sh
    fd 2
    """
    robot = Sprite()
    algo = RobotAlgorithm(robot, input)
    
    for _ in range(6):
        algo.run_next_command()
    
    print robot.get_commands() == ['r -90', 'r -90', 'r -90', 'sh 15', 'mv 1', 'mv 1']

test_basic_commands()
test_repeat_arg()