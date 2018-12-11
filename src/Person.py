import pygame


WIDTH = 1024
HEIGHT = 768
tile_size = 32
RED = (255, 0, 0)


class Person(pygame.sprite.Sprite):
    pos_min_x = 0
    pos_min_y = 0

    def __init__(self):
        super().__init__() #calls the constructor of the superclass sprite

    def display(self, screen):
        """
            Method that displays the person
            :param screen --> Display object where the person object will be display on
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def setPos(self, t):
        """
            Method that updates the position of the person, based on the time passed and the velocity of the person
            :param t --> time passed in seconds from the last call
        """
        # Here, the new position vector is calculated. The attibute rect is turned into a 2d vector class to make easier the operations
        newpos = pygame.math.Vector2(self.rect.x, self.rect.y) + self.vel * self.speed * t

        # once the new position is calculated,, we make sure that it is inside the boundaries of the screen
        newpos.x = clamp(newpos.x, Person.pos_min_x, self.pos_max_x)
        newpos.y = clamp(newpos.y, Person.pos_min_y, self.pos_max_y)
        self.pos = newpos
        self.rect.x = newpos.x
        self.rect.y = newpos.y

    def setVel(self, vec):
        """
            Method that update the velocity of the person
            :param vec: new vector velocity
        """
        if vec != (0.,0.):
        #if the new velocity vector is different from (0,0) we need to turn it into a unit vector to get only the direction of the movement
            self.vel = vec.normalize()
        else:
            self.vel = vec

    def collision_wall_y(self, wallx, wally):
        """
            Method that evaluate if there is any collision in the y axis between the object and a wall
            :param wallx: rect.centerx of the wall object
            :param wally: rect.centery of the wall object
            :return: the type of collision: "top", "bottom" or "none"
        """
        dist_center_xmin = self.img_width / 2 + tile_size / 2
        dist_center_ymin = self.img_height / 2 + tile_size / 2
        margin = 5

        if self.rect.centery > wally - dist_center_ymin and self.rect.centery < wally and self.rect.centerx > wallx - dist_center_xmin + margin and self.rect.centerx < wallx + dist_center_xmin - margin:
            return "top"
        elif self.rect.centery < wally + dist_center_ymin and self.rect.centery > wally and self.rect.centerx > wallx - dist_center_xmin + margin and self.rect.centerx < wallx + dist_center_xmin - margin:
            return "bottom"
        else:
            return "none"

    def collision_wall_x(self, wallx, wally):
        """
            Method that evaluate if there is any collision in the y axis between the object and a wall
            :param wallx: rect.centerx of the wall object
            :param wally: rect.centery of the wall object
            :return: the type of collision: "right", "left" or "none"
        """
        dist_center_xmin = self.img_width / 2 + tile_size / 2
        dist_center_ymin = self.img_height / 2 + tile_size / 2
        margin = 5
        if self.rect.centerx > wallx - dist_center_xmin and self.rect.centerx < wallx and self.rect.centery <= wally + dist_center_ymin - margin and self.rect.centery >= wally - dist_center_ymin + margin:
            return "left"
        elif self.rect.centerx < wallx + dist_center_xmin and self.rect.centerx > wallx and self.rect.centery <= wally + dist_center_ymin - margin and self.rect.centery >= wally - dist_center_ymin + margin:
            return "right"
        else:
            return "none"

    def get_time_hit(self):
        """
            Method that returns the moment of the last hit of the hero
        :return:
        """
        return pygame.time.get_ticks()

def clamp(n, minn, maxn):
    """
        Function that limit the value of a given variable between a max and a min
        Source:https://stackoverflow.com/questions/5996881/how-to-limit-a-number-to-be-within-a-specified-range-python
    """
    return max(min(maxn, n), minn)