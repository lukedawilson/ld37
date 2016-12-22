class RobotRuntimeException(BaseException):
    """
    Generic runtime exception for game interpreter
    """

class RobotAlgorithm:
    def __init__(self, robot, raw_program):
        self.robot = robot
        
        commands = self.__to_commands_list(raw_program)
        stack = self.__list_to_stack(commands)
        
        self.program = self.__translate(stack)        
        self.current_step = 0
        
    def run_next_command(self):
        if self.current_step >= len(self.program):
            self.current_step = 0   
    
        statement = self.program[self.current_step]
        cmd = statement[0]
        arg = statement[1] if len(statement) > 1 else ''     
        skip = statement[2] if len(statement) > 2 else 0
        
        while cmd == 'if':
            self.current_step += 1
            
            passed = self.__evaluate(arg)
            if passed == False:
                self.current_step += skip
                
            if self.current_step >= len(self.program):
                cmd = None
                break
                
            statement = self.program[self.current_step]
            cmd = statement[0]
            arg = statement[1] if len(statement) > 1 else ''     
            skip = statement[2] if len(statement) > 2 else 0
            
        if cmd == 'rl':
            self.robot.rotate(-90)
        elif cmd == 'rr':
            self.robot.rotate(90)
        elif cmd == 'fd':
            self.robot.move_forward()
        elif cmd =='sh':
            self.robot.shoot(15)
        else:
            raise RobotRuntimeException('Unknown command - {}'.format(cmd))
            
        self.current_step += 1
            
    def __evaluate(self, condition):
        value = not condition.startswith('!')
        condition = condition.strip('!')
    
        if condition == 'el':
            return self.robot.enemy_left() == value
        if condition == 'er':
            return self.robot.enemy_right() == value
        if condition == 'ef':
            return self.robot.enemy_front() == value
        if condition == 'fl':
            return self.robot.friend_left() == value
        if condition == 'fr':
            return self.robot.friend_right() == value
        if condition == 'ff':
            return self.robot.friend_front() == value
        if condition == 'wl':
            return self.robot.wall_left() == value
        if condition == 'wr':
            return self.robot.wall_right() == value
        if condition == 'wf':
            return self.robot.wall_front() == value
                            
        raise RobotRuntimeException('Unknown condition - {}'.format(condition))
                    
    def __translate(self, block, result=None, entry_condition=None):
        if not result:
            result = []
        
        while len(block) > 0:
            statement = filter(None, block.pop().split(' '))
            func = statement[0]
            arg = statement[1] if len(statement) > 1 else None
            
            if func == 'end':
                return result
            elif func == 'if':
                skip = self.__get_if_block_length(block)    
                result.append([func, arg, skip])
                self.__translate(block, result, arg)
            elif func == 'else':
                skip = self.__get_if_block_length(block)
                result.append(['if', '!{}'.format(entry_condition), skip])
                self.__translate(block, result)
                return result
            else:
                try:
                    count = int(arg) if arg else 1
                except ValueError:
                    raise RobotRuntimeException('Invalid argument - {}. Expected argument of type int.'.format(arg))
                    
                for _ in range(count):
                    result.append([func.strip()])
                    
        return result
                    
    def __get_if_block_length(self, block):
        section = self.__stack_to_list(block)
        ifs = 0
        ends = 0
        repeats = 0
        for i in range(0, len(section) - 1):
            inner = filter(None, section[i].split(' '))
            inner_cmd = inner[0]
            
            if inner_cmd == 'if':
                ifs += 1
            elif inner_cmd == 'end':
                if ifs == 0:
                    break
                
                ends += 1    
                ifs -= 1
            elif inner_cmd == 'else':
                if ifs == 0:
                    break
                
                ifs -= 1
            elif len(inner) > 1:
                inner_arg = inner[1]
                
                try:
                    repeats += (int(inner_arg) - 1)
                except ValueError:
                    raise RobotRuntimeException('Invalid argument - {}. Expected argument of type int.'.format(inner_arg))
   
        return i - ends + repeats
    
    def __stack_to_list(self, stack):
        return list(reversed(stack))
        
    def __list_to_stack(self, collection):
        return list(reversed(collection)) # in Python, pop() removes the last entry of the list
        
    def __to_commands_list(self, raw_program):
        return list(filter(None, map(lambda x: x.strip().lower(), raw_program.split('\n'))))