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
        self.commands.append('r {}'.format(str(angle)))
        
    def move_forward(self, direction=1): # 1=forward, -1=backwards, 0=sit on yer arse
        self.commands.append('mv {}'.format(str(direction)))
        
    def shoot(self, velocity=10):
        self.commands.append('sh {}'.format(str(velocity)))
        
    def enemy_left(self):
        return self.left
        
    def enemy_right(self):
        return self.right
        
    def enemy_front(self):
        return self.front
        
    def friend_left(self):
        return self.left
        
    def friend_right(self):
        return self.right
        
    def friend_front(self):
        return self.front
        
    def wall_left(self):
        return self.left
        
    def wall_right(self):
        return self.right
        
    def wall_front(self):
        return self.front 

def assert_are_equal(expected, actual):
   test = inspect.stack()[1][3]
   passed = expected == actual
   if passed:
       print '{} PASSED'.format(test)
   else:
       print '{} FAILED\n\nExpected:\n{}\n\nActual:\n{}'.format(test, str(expected), str(actual))

def test_basic_commands():
    # Arange
    input = """
    RL
    rr
    FD
    Sh
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
    if fl
        rl
        sh
    end
    if fr
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
    if wl
        rl
        sh
        if er
            rr
            sh
        end
        rl
    end
    if wf
        if el
            rr
        end
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
        rr 4
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
        fd 3
        if el
            rr 4
        end
    end
    rr 3
    """
    robot = Sprite(True, True)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(13):
        algo.run_next_command()
        
    assert_are_equal(['mv 1', 'mv 1', 'r -90', 'sh 15', 'sh 15', 'r 90', 'r 90', 'r 90', 'sh 15', 'r -90', 'r 90', 'r 90', 'r 90'], robot.get_commands())    

def test_if_else():
    # Arrange
    input = """
    fd
    if el
        rl 2
    else
        rr
        fd
    end
    sh
    if er
        fd
    else
        rr
    end
    sh
    """
    robot = Sprite(left=False, right=True)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(6):
        algo.run_next_command()
        
    assert_are_equal(['mv 1', 'r 90', 'mv 1', 'sh 15', 'mv 1', 'sh 15'], robot.get_commands())
    
def test_nested_if_else(left, right, forward, expected):
    # Arrange
    input = """
    fd
    if el
        rl
        sh 2
    else
        if er
            rr
            sh 3
        else
            if ef
                sh 4
            end
        end
    end
    fd
    """
    robot = Sprite(left, right, forward)
    algo = RobotAlgorithm(robot, input)
    
    # Act
    for _ in range(len(expected)):
        algo.run_next_command()
        
    assert_are_equal(expected, robot.get_commands())

test_basic_commands()
test_repeat_arg()
test_if()
test_nested_if()
test_if_with_repeat()
test_nested_if_with_repeat()
test_if_else()
test_nested_if_else(True, True, True, ['mv 1', 'r -90', 'sh 15', 'sh 15', 'mv 1'])
test_nested_if_else(False, True, True, ['mv 1', 'r 90', 'sh 15', 'sh 15', 'sh 15', 'mv 1'])
test_nested_if_else(False, False, True, ['mv 1', 'sh 15', 'sh 15', 'sh 15', 'sh 15', 'mv 1'])
