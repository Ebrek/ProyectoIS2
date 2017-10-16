
import pygame
 
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

class Level():
    def __init__(self, level, player_settings, bg_music):
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.bg = pygame.Surface((32,32))
        #self.bg =pygame.image.load("bg1.png")
        self.bg.convert()
        #self.bg.fill(Color("#000000")) 
        self.entities = pygame.sprite.Group()
        
        self.platforms = []

        x = y = 0
        self.level = level
        # build the level
        for row in level:
            for col in row:
                if col == "P":
                    p = Platform(x, y)
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "E":
                    e = ExitBlock(x, y)
                    self.platforms.append(e)
                    self.entities.add(e)
                x += 32
            y += 32
            x = 0
        self.total_level_width  = len(level[0])*32
        self.total_level_height = len(level)*32

        self.player = Player(player_settings[0],player_settings[1],player_settings[2])

        self.camera = Camera(Camera.complex_camera, self.total_level_width, self.total_level_height)
        self.entities.add(self.player)
        self.backGround = Background('bg1.png', [0,0], (1280, 720))

        self.playmusic(bg_music)
    def update(self, up, down, left, right, space, running):
        # draw background
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))

        self.camera.update(self.player)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.backGround.image, self.backGround.rect)
        # update player, draw everything else
        if(self.player.rect.y>self.total_level_height):
            return False
        self.player.update(up, down, left, right, space, running, self.platforms)
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
    def playmusic(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1, 0.0)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, screen_sizes):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (1280, 720))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Media_Screen():
    def __init__(self, timer, bg):
        self.timer = timer
        #self.bg=bg
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.timer.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self,text,size,color,x,y):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

class Start_Screen(Media_Screen):
    def __init__(self, timer):
        Media_Screen.__init__(self, timer,(Background('bg1.png', [0,0], (1280, 720))))
        self.screen=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.show_start_screen()
    def show_start_screen(self):
        # game splash/start screen
        image = pygame.image.load("logo.png")
        image = pygame.transform.scale(image,(550,200))
        image_width, image_height= image.get_size()
        #self.screen.fill("#0033FF")
        self.screen.blit(image,((WIN_WIDTH-image_width)/2,(WIN_HEIGHT-image_height)/3))
        self.draw_text("PRESS ANY KEY",32,(240,248,255),WIN_WIDTH/2,WIN_HEIGHT*3 /4)
        pygame.display.flip()
        self.wait_for_key()

def main():
    global cameraX, cameraY
    pygame.init()
    
    pygame.display.set_caption("Froggy!")
    timer = pygame.time.Clock()

    screen=Start_Screen(timer)

    up = down = left = right = space = running = False
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                                                                    P",
        "P                                                                                     ",
        "P                                                                                     ",
        "P                                                PPPPPPPPPPP                         P",
        "P                    PPPPPP                                             PPPPPP       P",
        "P                                                                                    P",
        "P                                                                                    P",
        "P    PPPPPPPP                                                                        P",
        "P                                                                                    P",
        "P                          PPPPPPP                           PPPPPP                  P",
        "P                                                                                    P",
        "P                                                                                    P",
        "P                                                                     PPPPPPP        P",
        "P                                                                                    P",
        "P                                     PPPPPP                                         P",
        "P                                                                                    P",
        "P                                                 PPPPPPPPPPP                        P",
        "P                                                                                    P",
        "P                 PPPPPPPPPPP                                                        P",
        "P                                                                                    P",
        "P                                                                                    P",
        "P                                                                                    P",
        "P                                                                                    E",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPP   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    player_settings = (32, 32, "froggy.png")
    level = Level(level, player_settings, 'bg_music1.ogg')
    

    done = play_again = False
    while not (done or play_again):
        timer.tick(60)

       
        for e in pygame.event.get():
            if e.type == QUIT: 
                done = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                paused = True#change for paused menu
                pause()
                pygame.event.clear()
                continue
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                space = False
        if(level.update(up, down, left, right, space, running)==False):
            play_again = True
        pygame.display.update()
    if(play_again):
        main()
    else:
        pygame.quit()
def pause():
    pygame.event.clear()
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def simple_camera(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

    def complex_camera(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y, image_path):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        #self.image = Surface((32,32))
        self._image_origin = pygame.image.load(image_path)
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False)
        self.image  = self._image_origin
        #self.image.fill(Color("#0000FF"))
        image_rect = (self.image.get_rect().size)
        self.image.convert()
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
        self.tongue = 0

    def update(self, up, down, left, right, space, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        #if running:
            #self.xvel = 12
        if left:
            self.xvel = -8
            self.image = self._image_toLeft
        if right:
            self.xvel = 8
            self.image = self._image_origin
        if space:
            if self.tongue <= 0:
                self.tongue = 20
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        if (self.tongue>=0):
            self.tongue-=1
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)


        a = Surface((32, 32))
        a.convert()
        a.fill(Color("#d8c217")) # change for image
        b = Rect(32, 32, 32, 32)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print ("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print ("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print ("collide top")

class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#d8c217")) # change for image
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))

if __name__ == "__main__":
    main()