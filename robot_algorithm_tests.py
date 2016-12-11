from robot_algorithm import RobotAlgorithm
import inspect

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

def assert_are_equal(expected, actual):
   print inspect.stack()[1][3] + ': ' + ('Passed' if expected == actual else 'Failed')

def test_basic_commands():
    # Arange
    input = """
    rl
    rr
    fd
    sh
    """
    robot = Sprite()
    algo = RobotAlgorithm(robot, input)

    # Act
    for _ in range(4):    
        algo.run_next_command()
    
    #Assert
    assert_are_equal(['r -90', 'r 90', 'mv 1', 'sh 15'], robot.get_commands())
    
def test_repeat_arg():
    # Arrange
    input = """
    rl 3
    sh
    fd 2
    """
    robot = Sprite()
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(6):
        algo.run_next_command()
    
    # Assert
    assert_are_equal(['r -90', 'r -90', 'r -90', 'sh 15', 'mv 1', 'mv 1'], robot.get_commands())
    
def test_if():
    # Arrange
    input = """
    fd
    if el
        rl
        sh
    end
    if er
        rr
        sh
    end
    fd
    """
    robot = Sprite(True)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(4):
        algo.run_next_command()
        
    assert_are_equal(['mv 1', 'r -90', 'sh 15', 'mv 1'], robot.get_commands())    
    
def test_nested_if():
    # Arrange
    input = """
    fd
    if el
        rl
        sh
        if er
            rr
            sh
        end
        rl
    end
    if ef
        fd
    end
    rr
    """
    robot = Sprite(True, True)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(7):
        algo.run_next_command()
        
    assert_are_equal(['mv 1', 'r -90', 'sh 15', 'r 90', 'sh 15', 'r -90', 'r 90'], robot.get_commands())    

def test_if_with_repeat():
     # Arrange
    input = """
    fd
    if el
        rl 3
        sh
    end
    if er
        rr
        sh
    end
    fd
    """
    robot = Sprite(True)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(6):
        algo.run_next_command()
        
    assert_are_equal(['mv 1', 'r -90', 'r -90', 'r -90', 'sh 15', 'mv 1'], robot.get_commands())    
    
    
def test_nested_if_with_repeat():
    # Arrange
    input = """
    fd 2
    if el
        rl
        sh 2
        if er
            rr 3
            sh
        end
        rl
    end
    if ef
        fd
    end
    rr 3
    """
    robot = Sprite(True, True)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(13):
        algo.run_next_command()
        
    assert_are_equal(['mv 1', 'mv 1', 'r -90', 'sh 15', 'sh 15', 'r 90', 'r 90', 'r 90', 'sh 15', 'r -90', 'r 90', 'r 90', 'r 90'], robot.get_commands())    


test_basic_commands()
test_repeat_arg()
test_if()
test_nested_if()
test_if_with_repeat()
test_nested_if_with_repeat()