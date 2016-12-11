class RobotAlgorithm:
    def __init__(self, robot, raw_program):
        self.robot = robot
        
        stack = self.__get_commands_stack(raw_program)
        self.program = []
        self.__compile(list(stack), self.program)
        
        self.i = 0
        
    def run_next_command(self):
        if self.i >= len(self.program):
            self.i = 0   
    
        statement = filter(None, self.program[self.i].split(' '))
        cmd = statement[0]
        arg = statement[1] if len(statement) > 1 else ''     
        skip = int(statement[2]) if len(statement) > 2 else 0
        
        while cmd == 'if':
            self.i = self.i + 1
            
            passed = self.__evaluate(arg)
            if passed == False:
                self.i = self.i + skip
                
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
        value = not condition.startswith('!')
        condition = condition.strip('!')
    
        if condition == 'el':
            return self.robot.enemy_left() == value
        if condition == 'er':
            return self.robot.enemy_right() == value
        if condition == 'ef':
            return self.robot.enemy_front() == value
            
        return False    
            
    def __compile(self, block, result, entry_condition=None):
        while len(block) > 0:
            statement = filter(None, block.pop().split(' '))
            func = statement[0]
            arg = statement[1] if len(statement) > 1 else ''
            
            if func == 'end':
                return
            elif func == 'if':
                section = list(reversed(block))
                ifs = []
                skip = 0
                ends = 0
                repeats = 0
                for skip in range(0, len(section) - 1):
                    inner = filter(None, section[skip].split(' '))
                    inner_cmd = inner[0]
                    
                    if inner_cmd == 'if':
                        ifs.insert(0, True)
                    elif inner_cmd == 'end':
                        if not ifs:
                            break
                        
                        ends = ends + 1    
                        ifs.pop()
                    elif inner_cmd == 'else':
                        if not ifs:
                            break
                            
                        ifs.pop()
                    elif len(inner) > 1:
                        inner_arg = inner[1]
                        repeats = repeats + int(inner_arg) - 1
                    
                    skip = skip + 1
                    
                result.append((func + ' ' + arg + ' ' + str(skip - ends + repeats)).strip())
                self.__compile(block, result, arg)
            elif func == 'else':
                section = list(reversed(block)) #TODO method
                ifs = []
                skip = 0
                ends = 0
                repeats = 0
                for skip in range(0, len(section) - 1):
                    inner = filter(None, section[skip].split(' '))
                    inner_cmd = inner[0]
                    
                    if inner_cmd == 'if':
                        ifs.insert(0, True)
                    elif inner_cmd == 'end':
                        if not ifs:
                            break
                        
                        ends = ends + 1    
                        ifs.pop()
                    elif inner_cmd == 'else':
                        if not ifs:
                            break
                        
                        ifs.pop()
                    elif len(inner) > 1:
                        inner_arg = inner[1]
                        repeats = repeats + int(inner_arg) - 1
                    
                    skip = skip + 1
            
                result.append(('if !' + entry_condition + ' ' + str(skip - ends + repeats)).strip())
                self.__compile(block, result)
                return
            else:
                count = int(arg) if arg <> '' else 1
                for _ in range(count):
                    result.append((func).strip())
        
    def __get_commands_stack(self, raw_program):
        return list(reversed(list(filter(None, map(lambda x: x.strip(), raw_program.split('\n'))))))