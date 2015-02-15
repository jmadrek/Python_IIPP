# program template for Spaceship
######################################################
#Imports
import simplegui
import math
import random

######################################################
# globals for user interface
#Constants
WIDTH = 800
HEIGHT = 600
CANVAS_SIZE = (WIDTH, HEIGHT)
ANGLE_ADJ = math.pi/30
FRICTION = 0.1
THRUST = 0.5
DETHRUST_FRIC = 0.15
SP_THRUST = 2
SP_ANG_ADJ = math.pi/60
MISSLE_MULT = 8
TEXT_Y =  35
TEXT_SIZE = 24
SCORE_X = WIDTH*0.75
LIVES_X = WIDTH*0.10
MIN_SPAWN_RANGE = 3
MISSIL_LIFE = 50
SCORE = 0
LIVES = 3
VEL_DIV = 30
EXP_LIFE = 24
EXP_MULT = 7
#Other Globals

time = 0.5
started = False
######################################################
#ImageInfo Class, loaded prior to other classes due to pythons linear nature
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

######################################################
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_brown.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, MISSIL_LIFE)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, EXP_LIFE*EXP_MULT, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

ship_explosion_info = ImageInfo([64, 64], [128, 128], 17, EXP_LIFE*EXP_MULT, True)
ship_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


######################################################
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

######################################################
#Other classes - Ship, Sprite
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound):
        self.pos = [pos[0],pos[1]]
        self.orig_pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.orig_vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle  = angle
        self.orig_angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.sound = sound
        self.lives = LIVES
        self.score = SCORE
     
    def respawn(self):
        self.lives -= 1
        explosions.add(Sprite(self.pos, self.vel, 0, 0, ship_explosion_image, ship_explosion_info, explosion_sound))
        return self.lives
    
    def reset(self):
        global started
        self.pos = self.orig_pos[:]
        self.vel = self.orig_vel[:]
        self.angle = self.orig_angle
        self.lives = LIVES
        self.score = SCORE
        started = False
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0]+self.image_size[0],self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        self.angle += self.angle_vel
        #v = (1-c)*vel + thrust
        forward = angle_to_vector(self.angle)
        for x in range(2):
            if self.thrust:
                self.vel[x] *= (1-FRICTION)
                self.vel[x] += (forward[x]*THRUST)
                self.sound.play()
            else:
                self.vel[x] *= (1-DETHRUST_FRIC*FRICTION)
            self.pos[x] = (self.pos[x] + self.vel[x])%CANVAS_SIZE[x]
    
    def adjust_angle_vel(self, adj):
        self.angle_vel += adj
        
    def set_thrust(self, mBool):
        self.thrust = mBool == 1
        if not self.thrust:
            self.sound.rewind()
    
    def adj_score(self, add):
        self.score += add
        
    def shoot(self, key_dir):
        global a_missile
        if key_dir == 1:
            mod = angle_to_vector(self.angle)
            pos = [0,0]
            vel = [0,0]
            forward = angle_to_vector(self.angle)
            for x in range(2):
                pos[x] = self.pos[x]+ mod[x]*float(self.image_size[1]/2)
                vel[x] = (self.vel[x] + MISSLE_MULT*forward[x])
            missiles.add(Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound))
            
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
        #i need to step through the tiles if animated
        if self.animated:
            m_index = (self.age%self.lifespan/EXP_MULT)//1
            self.image_center = [self.image_center[0] +  m_index * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += SP_ANG_ADJ*self.angle_vel   
        for x in range(2):
            self.pos[x] = (self.pos[x] + self.vel[x])%CANVAS_SIZE[x]

        self.age += 1
        return self.age < self.lifespan
            
    
    def collide(self, other_sprite):
        return dist(self.pos, other_sprite.pos) <= self.radius + other_sprite.radius
    
    
            
######################################################
#Event Handlers
def draw(canvas):
    global time, score
    
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH/2, HEIGHT/2), splash_info.get_size())
    else:
    
        # draw ship and sprites
        my_ship.draw(canvas)
    
        update_sprite_group(rocks, canvas)
        update_sprite_group(missiles, canvas)
        
        # update ship and sprites
        my_ship.update()
        
        #check collisions
        if group_collide(my_ship, rocks):
            if my_ship.respawn() <= 0:
                my_ship.reset()
                frame_reset()
        
        my_ship.adj_score(groups_collide(missiles, rocks))
    
    update_sprite_group(explosions, canvas)
        
    #Add text
    canvas.draw_text("Score " + str(my_ship.score), (SCORE_X, TEXT_Y), TEXT_SIZE, "White")
    canvas.draw_text("Lives " + str(my_ship.lives), (LIVES_X, TEXT_Y), TEXT_SIZE, "White")
    
######################################################.

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], (3/2.0)*math.pi, ship_image, ship_info, ship_thrust_sound)
rocks = set([])
missiles = set([])
explosions = set([])

#Missle and rock will become sets
######################################################
#Event handlers
# timer handler that spawns a rock    
def rock_spawner():
    global rocks
    if not started or len(rocks) >= 12:
        return None
    
    vel = [0,0]
    ang_dir = random.randrange(-1,2,2)
    #make sure the rock does not spawn on the ship or to close to it
    exit = False
    while not exit:
        pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        exit = dist(pos, my_ship.get_pos()) > asteroid_info.get_radius() + my_ship.get_radius()*MIN_SPAWN_RANGE
        
    for x in range(2):
        vel[x] = (random.randrange(-1*SP_THRUST,SP_THRUST+1)*(1 + my_ship.score/VEL_DIV))
    rocks.add(Sprite(pos, vel, 0, ang_dir, asteroid_image, asteroid_info))
     
def key_down(key):
    if key in KEY_EVENT:
        KEY_EVENT[key][FXN](KEY_EVENT[key][ACTION])

#Key Handlers
FXN = 0
ACTION = 1
KEY_EVENT = {simplegui.KEY_MAP["right"]: [my_ship.adjust_angle_vel,ANGLE_ADJ,],
          simplegui.KEY_MAP["left"]: [my_ship.adjust_angle_vel,-1*ANGLE_ADJ],
          simplegui.KEY_MAP["up"]: [my_ship.set_thrust,1],
          simplegui.KEY_MAP["space"]: [my_ship.shoot, 1 ]}

def key_up(key):
    if key in KEY_EVENT:
        KEY_EVENT[key][FXN](-1*KEY_EVENT[key][ACTION])
    
def group_collide(obj, sprite_set):
    for sprite in list(sprite_set):
        if sprite.collide(obj):
            explosions.add(Sprite(sprite.pos, sprite.vel, 0, 0, explosion_image, explosion_info, explosion_sound))
            sprite_set.remove(sprite)
            return True
    return False

def groups_collide(sprite_set1,sprite_set2):
    #want to return number of collisions
    return_count = 0
    for sprite in list(sprite_set1):
        if group_collide(sprite, sprite_set2):
            sprite_set1.remove(sprite)
            return_count += 1
     
    return return_count

def update_sprite_group(spr_grp, canvas):
    for sprite in list(spr_grp):
        sprite.draw(canvas)
        if not sprite.update():
            spr_grp.remove(sprite)
           
    
    
def mouse_click(position):
    global started
    if started:
        return None
    
    start = [False, False]
    for x in range(2):
        start[x] = (position[x] < CANVAS_SIZE[x] - (splash_info.get_size()[x]/2.0)
                and position[x] > (splash_info.get_size()[x]/2.0))
    started = start[0] and start[1]
    
    if started:
        soundtrack.rewind()
        soundtrack.play()
            

    
def frame_reset():
    global rocks, missiles, time, explosions
    time = 0.5
    rocks = set([])
    missiles = set([])
    soundtrack.pause()
    
######################################################
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
######################################################

######################################################
# register handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouse_click)
######################################################
# get things rolling
timer.start()
frame.start()
