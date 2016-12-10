#TODO this is a stub of your Robot class - replace with import of real thing
class Robot:
    def rotate(self, angle):
        print 'Rotate ' + str(angle) + ' degrees'
        
    def move_forward(self, direction=1): # 1=forward, -1=backwards, 0=sit on yer arse
        print 'Move ' + ('forwards' if 1 else ('backwards' if -1 else 'nowhere'))
        
    def shoot(self, velocity=10):
        print 'Shoot at ' + str(velocity) + ' velocity'
        
    def enemy_left(self):
        return True
        
    def enemy_right(self):
        return False
        
    def enemy_front(self):
        return True
        
    def wall_front(self):
        return False
        
    def dead(self):
        return False