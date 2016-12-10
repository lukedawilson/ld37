import switch
from robot import Sprite

class RobotAlgorithm:
    def __init__(self, robot, raw_program):
        self.robot = robot
        
        stack = self.__parse_program(raw_program) # stack
        self.program = []
        self.__parse(list(stack), self.program)

        self.i = 0
        
    def run_next_command(self):
        if self.i >= len(self.program):
            self.i = 0   
    
        statement = filter(None, self.program[self.i].split(' '))
        cmd = statement[0]
        arg = statement[1] if len(statement) > 1 else ''     
        skip = int(statement[2]) if len(statement) > 2 else 0
        
        while cmd == 'if':
            passed = self.__evaluate(arg)
            if passed == False:
                self.i = self.i + skip
                
            self.i = self.i + 1
            if self.i >= len(self.program):
                cmd = None
                break
                
            statement = filter(None, self.program[self.i].split(' '))
            cmd = statement[0]
            arg = statement[1] if len(statement) > 1 else ''     
            skip = int(statement[2]) if len(statement) > 2 else 0
            
        if cmd == 'rl':
            self.robot.rotate(-90)
        elif cmd == 'rr':
            self.robot.rotate(90)
        elif cmd == 'fd':
            self.robot.move_forward()
        elif cmd =='sh':
            self.robot.shoot(15)
            
        self.i = self.i + 1
            
    def __evaluate(self, condition):
        if condition == 'el':
            return self.robot.enemy_left()
        if condition == 'er':
            return self.robot.enemy_right()
        if condition == 'ef':
            return self.robot.enemy_front()
            
        return False    
            
    def __parse(self, block, result):
        while len(block) > 0:
            statement = filter(None, block.pop().split(' '))
            func = statement[0]
            arg = statement[1] if len(statement) > 1 else ''
            
            if func == 'end':
                return
            
            if func <> 'if':
                result.append((func + ' ' + arg).strip())
            else:
                section = list(reversed(block))
                ifs = []
                skip = 0
                for skip in range(0, len(section) - 1):
                    next = filter(None, section[skip].split(' '))
                    if next[0] == 'if':
                        ifs.insert(0, True)
                    elif next[0] == 'end':
                        if not ifs:
                            break
                            
                        ifs.pop()
                        
                    skip = skip + 1
                    
                result.append((func + ' ' + arg + ' ' + str(skip)).strip())
                self.__parse(block, result)
        
    def __parse_program(self, raw_program):
        return list(reversed(list(filter(None, raw_program.split('\n')))))