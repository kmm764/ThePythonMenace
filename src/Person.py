



class Person(pygame.sprite.Sprite):

    pos_max_x=WIDTH-img_width
    pos_max_y=HEIGHT-img_height
    pos_min_x=0
    pos_min_y=0

    def __init__(self):
        super().__init__()

    def display(self, displayObj):
        """
            Method that displays the hero
            :param displayObj --> Object display where the person will be display on
        """
        displayObj.blit(self.image, (self.rect.x, self.rect.y))

    def setPos(self, t):
        """
            Method that updates the position of the hero, based on the time passed and the velocity of the hero
            :param t --> time passed in seconds from the last call
        """
        #Here, the new position vector is calculated. The attibute rect is turned into a 2d vector class to make easier the operations


        newpos =  pygame.math.Vector2(self.rect.x, self.rect.y)+self.vel*self.speed*t

        #once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x=clamp(newpos.x,Person.pos_min_x,Person.pos_max_x)
        newpos.y=clamp(newpos.y, Person.pos_min_y, Person.pos_max_y)
        self.pos = newpos
        self.rect.x = newpos.x
        self.rect.y = newpos.y

    def setVel(self, vec):
        """
            Method that update the velocity of the hero
            :param vec: new vector velocity
        """
        if vec != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vec.normalize()
        else:
        #if the new velocity vector is (0,0)
            self.vel=vec

def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
        Source:https://stackoverflow.com/questions/5996881/how-to-limit-a-number-to-be-within-a-specified-range-python
    """
    return max(min(maxn, n), minn)