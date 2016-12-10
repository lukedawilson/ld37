#TODO this is a stub of your Robot class - replace with import of real thing
class Robot:
    def rotate(self, angle):
        print 'Rotate ' + str(angle) + ' degrees'
        
    def move_forward(self, direction=1): # 1=forward, -1=backwards, 0=sit on yer arse
        print 'Moved in the ' + str(direction) + ' direction'    
        
    def shoot(self, velocity=10):
        print 'Shoot at ' + str(velocity) + ' velocity'
        
    def enemy_left(self):
        return true
        
    def enemy_right(self):
        return false;
        
    def enemy_front(self):
        return true
        
    def wall_front(self):
        return false
        
    def dead(self):
        return false