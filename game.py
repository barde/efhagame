###################################################################################
###################################################################################
# efhagame -  by Bartholomaeus Dedersen
# based on:
# Sprite Movement Towards Target Example + Physics
# programed/documented by Mad Cloud Games
# contact Mad Cloud Games @ madcloudgames@gmail.com with any comments, questions, or changes
#
# This project is released under the GNU General Public License V3
# This code is open source
# We would love to know what it gets used for
###################################################################################
###################################################################################

import pygame, math
from pygame.locals import *
pygame.init()

screenwidth = 800
screenheight = 600

class Vector():
    '''
        Class:
            creates operations to handle vectors such
            as direction, position, and speed
        '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self): # used for printing vectors
        return "(%s, %s)"%(self.x, self.y)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("This "+str(key)+" key is not a vector key!")

    def __sub__(self, o): # subtraction
        return Vector(self.x - o.x, self.y - o.y)

    def length(self): # get length (used for normalize)
        return math.sqrt((self.x**2 + self.y**2)) 

    def normalize(self): # divides a vector by its length
        l = self.length()
        if l != 0:
            return (self.x / l, self.y / l)
        return None



class Sprite(pygame.sprite.Sprite):
    
    def __init__(self):
        '''
        Class:
            creates a sprite
        Parameters:
            - self
        '''
        self.image = pygame.image.load("zombie.png").convert_alpha() # load image
        self.rect = self.image.get_rect()

        self.reset_position()
        self.speed = 3 # movement speed of the sprite

        self.normal_friction = .95 # friction while accelerating
        self.slowing_friction = .8 # friction while slowing down

        self.target = None # starts off with no target

    def reset_position(self):
        self.trueX = screenwidth / 2 # created because self.rect.center does not hold
        self.trueY = screenheight - 50# decimal values but these do
        self.rect.center = (self.trueX, self.trueY) # set starting position
        self.speedX = 0 # speed in x direction
        self.speedY = 0 # speed in y direction
        self.target = None

    def get_direction(self, target):
        '''
        Function:
            takes total distance from sprite.center
            to the sprites target
            (gets direction to move)
        Returns:
            a normalized vector
        Parameters:
            - self
            - target
                x,y coordinates of the sprites target
                can be any x,y coorinate pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        if self.target: # if the square has a target
            position = Vector(self.rect.centerx, self.rect.centery) # create a vector from center x,y value
            target = Vector(target[0], target[1]) # and one from the target x,y
            self.dist = target - position # get total distance between target and position

            direction = self.dist.normalize() # normalize so its constant in all directions
            return direction
        
    def distance_check(self, dist):
        '''
        Function:
            tests if the total distance from the
            sprite to the target is smaller than the
            ammount of distance that would be normal
            for the sprite to travel
            (this lets the sprite know if it needs
            to slow down. we want it to slow
            down before it gets to it's target)
        Returns:
            bool
        Parameters:
            - self
            - dist
                this is the total distance from the
                sprite to the target
                can be any x,y value pair in
                brackets [x,y]
                or parentheses (x,y)
        '''
        dist_x = dist[0] ** 2 # gets absolute value of the x distance
        dist_y = dist[1] ** 2 # gets absolute value of the y distance
        t_dist = dist_x + dist_y # gets total absolute value distance
        speed = self.speed ** 2 # gets aboslute value of the speed

        if t_dist < (speed): # read function description above
            return True
        

    def update(self):
        '''
        Function:
            gets direction to move then applies
            the distance to the sprite.center
            ()
        Parameters:
            - self
        '''
        
        self.dir = self.get_direction(self.target) # get direction
        if self.dir: # if there is a direction to move
            
            if self.distance_check(self.dist): # if we need to slow down
                self.speedX += (self.dir[0] * (self.speed / 2)) # reduced speed
                self.speedY += (self.dir[1] * (self.speed / 2))
                self.speedX *= self.slowing_friction # increased friction
                self.speedY *= self.slowing_friction
                
            else: # if we need to go normal speed
                self.speedX += (self.dir[0] * self.speed) # calculate speed from direction to move and speed constant
                self.speedY += (self.dir[1] * self.speed)
                self.speedX *= self.normal_friction # apply friction
                self.speedY *= self.normal_friction

            self.trueX += self.speedX # store true x decimal values
            self.trueY += self.speedY
            self.rect.center = (round(self.trueX),round(self.trueY)) # apply values to sprite.center
                
class MovementDesignator():
    def __init__(self,screen):
        self.screen = screen # get the screen as main surface
        self.percent = 100 # scaled from 1-100: max value is real 246 pixel

    def update(self):
        pygame.draw.rect(self.screen,[0,255,0],[20,20,204,30],2)
        if self.percent:
            self.realValue = 2 * self.percent
            pygame.draw.line(self.screen, (255,0,0),(22,35),(self.realValue + 22,35), 27) # surface, color of lines, uhh, points of lines, width of lines)

    def get_graph_value(self):
        return self.percent

    def increase_graph(self):
        if self.percent < 100:
            self.percent += 10

    def decrease_graph(self):
        if self.percent > 0:
            self.percent -= 10



def main():

    screen = pygame.display.set_mode((screenwidth,screenheight))
    pygame.display.set_caption("efhagame - Hit all Brains")
    background_color = pygame.Surface(screen.get_size()).convert()
    background_color.fill((0,0,0))

    line_points = [] # make a list for points
    line_color = (0, 255, 255) # color of the lines

    sprite = Sprite() # create the sprite

    designator = MovementDesignator(screen)

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN:
                sprite.target = event.pos # set the sprite.target to the mouse click position
                line_points.append(event.pos) # add that point to the line list
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    sprite.reset_position()
                    line_points.append([screenwidth / 2, screenheight - 50])
                if event.key == K_UP:
                    designator.increase_graph()
                if event.key == K_DOWN:
                    designator.decrease_graph()
                
        screen.blit(background_color, (0,0))
        
        
        designator.update()

        sprite.update() # update the sprite
        screen.blit(sprite.image, sprite.rect.topleft) # blit the sprite to the screen
        
        if len(line_points) > 1: # if there are enough points to draw a line
            pygame.draw.lines(screen, line_color, False, line_points, 2) # surface, color of lines, uhh, points of lines, width of lines)

        pygame.display.flip()
    
    pygame.quit() # for a smooth quit
if __name__ == "__main__":
    main()
