import switch
from robot import Robot

#TODO this is a stub
class RobotAlgorithm:
    def __init__(self, robot, raw_program):
        self.robot = robot
        self.program = self.__parse_program(raw_program) # stack
        self.current_run = []

    def run_next_command(self):
        if self.__eof():
            self.current_run = list(self.program)
    
        step = self.current_run.pop()
        if step == 'rl':
            self.robot.rotate(-90)
        elif step == 'rr':
            self.robot.rotate(90)
        elif step == 'fd':
            self.robot.move_forward()
        elif step =='sh':
            self.robot.shoot(15)
            
    def __eof(self):
        return not self.current_run
        
    def __parse_program(self, raw_program):
        return list(reversed(list(filter(None, raw_program.split('\n')))))