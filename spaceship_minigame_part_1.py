# Minproject was done in Safari web browser

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
# ship with thrusters
ship_info_thrusters = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")


# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.state = False
        self.vel_vector = [1,1]
        

        
    def draw(self,canvas):
        canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    def inc_angle_vel(self):
        self.angle_vel = -.5
        self.angle += self.angle_vel
        # print self.angle, self.angle_vel
    
    def dec_angle_vel(self):
        self.angle_vel = .5
        self.angle += self.angle_vel
        # print self.angle, self.angle_vel
        
    def thrusters_active(self, state):
        global ship_info, ship_info_thrusters
        self.state = state
        if state == True:
            self.image_center = ship_info_thrusters.get_center()
            self.image_size = ship_info_thrusters.get_size()
            self.radius = ship_info_thrusters.get_radius()
            ship_thrust_sound.play()
        else:
            self.image_center = ship_info.get_center()
            self.image_size = ship_info.get_size()
            self.radius = ship_info.get_radius()
            if ship_thrust_sound:
                ship_thrust_sound.rewind()
            
            
                
        
    def update(self):
        if self.state:
            angle_vector = angle_to_vector(self.angle)
            acceleration = 2
            vel_vector = [angle_vector[0] * acceleration, angle_vector[1] * acceleration]
            self.pos[0] += vel_vector[0]
            self.pos[1] += vel_vector[1]
        else:
            angle_vector = angle_to_vector(self.angle)
            vel_vector = [angle_vector[0], angle_vector[1]]
            friction_const = .25
            vel_vector[0] *= friction_const
            vel_vector[1] *= friction_const
            self.pos[0] += vel_vector[0]
            self.pos[1] += vel_vector[1]
        
        # print "vel " + str(vel_vector[0])
        # print self.pos[1]
        # enable screen wrapping left and right sides
        if self.pos[0] % 800 < 10:
            # wrapping from right to left
            if self.pos[0] >= 800:
                # print "clear"
                self.pos[0] = 5
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
            # wrapping from left to right
            elif self.pos[0] <= 2:
                # print "clear"
                self.pos[0] = 795
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
        # enable screen wrapping top and bottom
        if self.pos[1] % 600 < 10:
            # wrapping from bottom to top
            if self.pos[1] >= 600:
                # print "clear"
                self.pos[1] = 5
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
            # wrapping from top to bottom
            elif self.pos[1] <= 2:
                # print "clear"
                self.pos[1] = 595
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
                
    def shoot(self):
        global a_missile, missile_sound
        angle_vector = angle_to_vector(self.angle)
        angle_vector_multiple = [angle_vector[0] * 45, angle_vector[1] * 45]
        pos = [self.pos[0], self.pos[1]]
        vel =  [self.vel[0] * angle_vector_multiple[0], self.vel[1] * angle_vector_multiple[1]]
        pos[0] += vel[0]
        pos[1] += vel[1]
        a_missile = Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_sound.play()

    
    def __str__(self):
        pass
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_center, self.angle)

    
    def update(self):
        # move asteroids
        self.angle += self.angle_vel
        angle_vector = angle_to_vector(self.angle)
        vel_vector = [angle_vector[0], angle_vector[1]]
        self.pos[0] += vel_vector[0]
        self.pos[1] += vel_vector[1]
        
        if self.pos[0] % 800 < 10:
            # wrapping from right to left
            if self.pos[0] >= 800:
                # print "clear"
                self.pos[0] = 5
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
            # wrapping from left to right
            elif self.pos[0] <= 2:
                # print "clear"
                self.pos[0] = 795
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
        # enable screen wrapping top and bottom
        if self.pos[1] % 600 < 10:
            # wrapping from bottom to top
            if self.pos[1] >= 600:
                # print "clear"
                self.pos[1] = 5
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]
            # wrapping from top to bottom
            elif self.pos[1] <= 2:
                # print "clear"
                self.pos[1] = 595
                self.pos[0] += vel_vector[0]
                self.pos[1] += vel_vector[1]        

           
    
def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives: " + str(lives), (WIDTH / 7, HEIGHT / 7), 32, "white", "serif")
    canvas.draw_text("Score: " + str(score), (WIDTH * 5 / 7, HEIGHT *  1 / 7), 32, "white", "serif")

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
# set event handlers
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    angle = random.random() * 3
    angle_vel = .1
    pos = [random.randrange(0, 800), random.randrange(0, 600)]
    vel = [random.random() * 2, random.random() * 2]
    a_rock = Sprite(pos, vel, angle, angle_vel, asteroid_image, asteroid_info)


    

# set key handlers
def key_down_handler(key):
    global thrusters
    # ship controllers
    if simplegui.KEY_MAP["left"] == key:
        my_ship.inc_angle_vel()
        # print "left"
    if simplegui.KEY_MAP["right"] == key:
        my_ship.dec_angle_vel()
        # print "right"
        
    # thrusters Flag    
    if simplegui.KEY_MAP["up"] == key:
        # print "Thrusters on"
        my_ship.thrusters_active(True)
        
    if simplegui.KEY_MAP["space"] == key:
        # print "shots fired"
        my_ship.shoot()

def key_up_handler(key):
    global thrusters
    # ship controllers
    if simplegui.KEY_MAP["left"] == key:
        pass
    elif simplegui.KEY_MAP["right"] == key:
        pass
    
    # thrusters Flag
    if simplegui.KEY_MAP["up"] == key:
        # print "thrusters off"
        my_ship.thrusters_active(False)
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [1, 1], -1.6, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()