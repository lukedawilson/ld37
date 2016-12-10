from robot import Robot

#TODO this is a stub
class RobotAlgorithm:
    def __init__(self, robot):
        self.robot = robot

    def run_next_command(self):
        self.robot.rotate(-90)
        #self.robot.move_forward(1)
        #self.robot.shoot(15)

# Example usage
robot = Robot()
algo = RobotAlgorithm(robot)
algo.run_next_command()