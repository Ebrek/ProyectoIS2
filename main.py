# -*- coding: utf-8 -*-
import pygame, sys, os
from PIL import Image, ImageOps
import numpy
from pygame import *
import math
import _thread
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

WHITE = (255, 255, 255)
OLIVE = (107, 142, 35)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

IMAGE_SIZES = {}
IMAGES = {}
PATH = "Resources/"

class Level():
    def __init__(self, level, player_settings, bg_music):
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.bg = pygame.Surface((32,32))
        self.bg.convert()
        self.entities = pygame.sprite.Group()

        self.platforms = []
        self.decorations = []
        self.enemies = []
        ########################################################nuevo
        self.gemas = []
        ########################################################
        x = y = 0
        self.level = level
        # build the level

        for row in level:
            for col in row:
                if col == "1":
                    p = Platform(x, y, "platform/jungle_pack_07.png")
                    self.platforms.append(p)
                    self.entities.add(p)

                if col == "2":
                    p = Platform(x, y, "platform/jungle_pack_35.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "P":
                    p = Platform(x, y, "platform/jungle_pack_05.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "3":
                    p = Platform(x, y, "platform/jungle_pack_03.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "4":
                    p = Platform(x, y, "platform/jungle_pack_11.png")
                    self.platforms.append(p)
                    self.entities.add(p)

                if col == "5":
                    p = Platform(x, y, "platform/jungle_pack_19.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "6":
                    p = Platform(x, y, "platform/jungle_pack_21.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "7":
                    p = Platform(x, y, "platform/jungle_pack_40.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "E":
                    e = ExitBlock(x, y)
                    self.platforms.append(e)
                    self.entities.add(e)
                if col == "Q":
                    q = EnemyMosquito(x, y)
                    self.enemies.append(q)
                    self.entities.add(q)
                if col == "S":
                    s = EnemySpider(x, y)
                    self.enemies.append(s)
                    self.entities.add(s)

                if col == "0":
                    p = Platform(x, y, "platform/jungle_pack_09.png")
                    self.platforms.append(p)
                    self.entities.add(p)

                if col == "D":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_67.png")
                    self.decorations.append(d)
                    self.entities.add(d)

                    #GEMAS
                    ########################################################
                if col == "G":
                    g = Gemas(x, y, 16,16, "items/gem_9.png")
                    self.gemas.append(g)
                    self.entities.add(g)
                    ########################################################

                if col == "!":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_59.png")
                    self.decorations.append(d)
                    self.entities.add(d)
                if col == "¡":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_57.png")
                    self.decorations.append(d)
                    self.entities.add(d)
                if col == "B":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_66.png")
                    self.decorations.append(d)
                    self.entities.add(d)

                #player
                if col == "F":
                    self.player = Player(x, y, player_settings[2])
                x += 32
            y += 32
            x = 0
        self.total_level_width  = len(level[0])*32
        self.total_level_height = len(level)*32

        self.camera = Camera(Camera.complex_camera, self.total_level_width, self.total_level_height)
        self.entities.add(self.player)

        self.backGround = Background(PATH+'platform/bg_jungle.png', [0,0], (1280, 720))
        try:
            self.playmusic(bg_music)
        except Exception:
            print("no bg music")
    def update(self, up, down, left, right, space, running):
        # draw background
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))

        self.camera.update(self.player)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.backGround.image, self.backGround.rect)
        # update player, draw everything else
        if not self.player.update(up, down, left, right, space, running, self.platforms, self.enemies, self.entities, self.gemas, self.total_level_width, self.total_level_height):
            return False
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

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=WHITE, pos_x = 0, pos_y = 0):

        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def is_mouse_selection(self, posx, posy):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)

class GameMenu():
    def __init__(self, screen, items, funcs, bg_color=BLACK, font=None, font_size=30,
                 font_color=WHITE):
        self.mainloop = True
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 1.25) - (t_h / 1.25) + ((index*1.25) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_keyboard_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(WHITE)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(OLIVE)

        # Finally check if Enter or Space is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text](self)

    def set_mouse_selection(self, item, mposx, mposy):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mposx, mposy):
            item.set_font_color(OLIVE)
            item.set_italic(True)
        else:
            item.set_font_color(WHITE)
            item.set_italic(False)

    def run(self):
        self.mainloop = True
        while self.mainloop:

            self.clock.tick(50)

            mposx, mposy = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("quit")
                    #self.mainloop = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mposx, mposy):
                            self.funcs[item.text](self)

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background
            self.screen.fill(self.bg_color)
            image = pygame.image.load(PATH+"logo.png")
            image = pygame.transform.scale(image,(450,200))
            image_width, image_height= image.get_size()
            self.screen.blit(image,((WIN_WIDTH-image_width)/3,(WIN_HEIGHT-image_height)/6))


            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mposx, mposy)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()


def iniciar(param):
    param.mainloop=False
    print(param.mainloop)
def mostrar_creditos(param):
    print("Creditos")
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
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self,text,size,color,x,y):
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

'''class Start_Screen(Media_Screen):
    def __init__(self, timer):
        Media_Screen.__init__(self, timer,(Background(PATH+'platform/bg_jungle.png', [0,0], (1280, 720))))
        self.screen=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.show_start_screen()
    def show_start_screen(self):
        # game splash/start screen
        image = pygame.image.load(PATH+"logo.png")
        image = pygame.transform.scale(image,(550,200))
        image_width, image_height= image.get_size()
        self.screen.blit(image,((WIN_WIDTH-image_width)/2,(WIN_HEIGHT-image_height)/3))
        self.draw_text("PRESS ANY KEY",32,(240,248,255),WIN_WIDTH/2,WIN_HEIGHT*3 /4)
        pygame.display.flip()
        self.running = True
        self.wait_for_key()
        if not self.running:
            pygame.quit()
            sys.exit()'''
def main():
    global cameraX, cameraY
    pygame.init()


    screen = pygame.display.set_mode((640, 480), 0, 32)
    menu_items = ('Iniciar', 'Mostrar Creditos', 'Salir')
    funcs = {'Iniciar': iniciar,
             'Mostrar Creditos' : mostrar_creditos,
             'Salir': sys.exit}

    pygame.display.set_caption("Froggy!")
    timer = pygame.time.Clock()
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()

    up = down = left = right = space = running = False
    #para cambiar niveles cambiar el nombre a level (no duplicados)
    level0 = [# level de testeo
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                             Q                   G           ",
        "              2    2  22222 2      222      22  22 2   2 22  2 222  2222                                       3PPP1         ",
        "              2    2  2   2 2     22 22     222222 2   2 222 2 2  2 2  2                                PPP    22222         ",
        "              222222  2   2 2     2   2     2 22 2 2   2 2 2 2 2  2 2  2                      D  GG            22222         ",
        "              2    2  2   2 2     22222     2    2 2   2 2 2 2 2  2 2  2                   3PPPPPPP1           22222        E",
        "              2    2  22222 22222 2   2     2    2 22222 2  22 222  2222                   222222222           22222PPPPPPPPP",
        "                                                                                           222222222           22222222222222",
        "                  GGG                                                                 B    222222222           22222222222222",
        "               PPPPPPPPP                                                      S    3PPPPPPP222222222           22222222222222",
        "               2       2                                                  3PPPPPPPP22222222222222222           22222222222222",
        "               2  Q    2                                              !   22222222222222222222222222           22222222222222",
        "               2       2                             B               3PPPP22222222222222222222222222           22222222222222",
        "          P     PPPPPPP       PP                5PPPPPP7          0PP2222222222222222222222222222222           22222222222222",
        "                                        B G      666666             66662222222222222222222222222222           22222222222222",
        "                                      PPPPPP                            6666222222222222222222222222           22222222222222",
        "        P                             622226                                662222222222222222222222           22222222222222",
        "                                       6666                                   6666666666666222222222           22222222222222",
        "                                                                               GGGGG       222222222           22222222222222",
        "    ¡  F     !  Q             S P  S  PB  GG  D     ¡                   D      GGGGG       222222222           22222222222222",
        "PPPPPPPPPPPPPPPPPP1          3PP2PPPPP2PPPPPPPPPPPPPPP1        P     3PPPPPPPPPPPPPPPPPPPP2222222222           22222222222222"]
    #levels
    level6 = [
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                             Q                   GG          ",
        "                                                                                                               3PPP1         ",
        "                                                                                                               22222         ",
        "                                                                                              D                22222         ",
        "                                                                                           3PPPPPPP1           22222         ",
        "                                                                                           222222222           22222PPPPPPPPP",
        "                                                                                           222222222           22222222222222",
        "                                                                                      B    222222222           22222222222222",
        "                                                                              S    3PPPPPPP222222222           22222222222222",
        "                                                                          3PPPPPPPP22222222222222222           22222222222222",
        "                                                                      !   22222222222222222222222222           22222222222222",
        "                                                   B                 3PPPP22222222222222222222222222           22222222222222",
        "                                                5PPPPPP7          0PP2222222222222222222222222222222           22222222222222",
        "                                        B        666666             66662222222222222222222222222222           22222222222222",
        "                                      PPPPPP                            6666222222222222222222222222           22222222222222",
        "                                      622226                                662222222222222222222222           22222222222222",
        "                                       6666                                   6666666666666222222222           22222222222222",
        "                                                                                   GGGG    222222222           22222222222222",
        "    ¡  F     !                   B    GGGG  D     ¡                     D          GGGG    222222222           22222222222222",
        "PPPPPPPPPPPPPPPPPP1         3PPPPPPPPPPPPPPPPPPPPPPPP1         P     3PPPPPPPPPPPPPPPPPPPP2222222222           22222222222222"]

    level3= [
        "                                                                                                                              ",
        "                                                                                                                              ",
        "                                                              G                                                               ",
        "                                     Q                   G       G                 Q                                          ",
        "                                                        G            G                                                        ",
        "                                                                                                                              ",
        "                                            B  S                             S B                                              ",
        "                                3PPPPPPPPPPPPPPPPPPPP1                3PPPPPPPPPPPPPPPPPPPP1                                  ",
        "                       G        6666666222222222222222                2222222222222222666666                                  ",
        "                      PPP              666666666666666                6666666666666666            PPP                         ",
        "                      666                                                                         666                         ",
        "                                   Q                         Q                         Q                                      ",
        "                  G                                                                                                           ",
        "           GG    PPP                           GG                         GG                          PPP                     ",
        "                 666                                                                                  666                     ",
        "  F!                             GG  B  GG            GGG   B  S  GGG           D   S GG                             ¡       E",
        "PPPPPPPPPPPP1                  3PPPPPPPPPPP1        3PPPPPPPPPPPPPPPPP1        3PPPPPPPPPPP1                     3PPPPPPPPPPPP",
        "2222222266666        GGG       6666662222222        2222222222222222222        2222222266666                     6666622222222",
        "22226666             PPP             6666666        6666666666666666666        66666666         PPP                   22222222",
        "6666                 666                                                                        666                   22222222",
        "                                                                                                                      22222222",
        "                                                  Q                                                                   22222222",
        "              PPP                                                                                       PPP           22222222",
        "              666                                                                                       666           22222222",
        "                                        GG            GG            GG              GG                                22222222",
        "                          B                                                                    B                      22222222",
        "                       3PPPPP1  S              B              GG          GG              S   3PPPPP1                 22222222",
        "                       6666662PPPPPPP1      3PPPPPP1        3PPP1      3PPPPPP1         PPPPPP2666666                 22222222"]



    levelx =  [
        "                                                                                                                                 ",
        "                                                                                                                                 ",
        "                                                                                                                                 ",
        "                                                                                                                                 ",
        "                                                                                                                                 ",
        "                                                                                                                                 ",
        "                                                                                                                                 ",
        "    F !         Q                  S                                                                                             ",
        "PPPPPPPPPPPP1            3PPPPPPPPPP1                                                                                            ",
        "2222222266666            666666666666                                                                                            ",
        "22226666                                                                                                                         ",
        "666                                                                                                                              ",
        "                                                                                                                                 ",
        "                                                  Q                                                                   S   GGGGG  ",
        "                                                                                 Q                       3P          3PPPPPPPPPPP",
        "                                              3PPPPPPP1                                        31        66P         666666666666",
        "                                              666666666                                        22          6P                    ",
        "                                                                                          31   22           6P                   ",
        "                                                                                          22   22            6P                  ",
        "                                                                                     31   22   22             6P                 ",
        "                                                                                     22   22   22              6P                ",
        "                                                                                31   22   22   22               6P               ",
        "                                                                 !  S           22   22   22   22                                ",
        "                                                               3PPPPPPPP1       22   22   22   22          S                  E  ",
        "                                                             3P2222222222       22   22   22   22         3PPPPPPPPPPPPPPPPPPPPPP",
        "GGGGGGGGG3PPPP1                     GG   D                  3222222222222       22   22   22   22         22222222222222222222222",
        "GGGGGPPPP222222                3PPPPPPPPPPPP1             3P2222222222222       22   22   22   22         22222222222222222222222",
        "PPPPPP222222222              3P22222222222222P3           222222222222222       22   22   22   22         22222222222222222222222"]




    level = [
        " S S S S  S          22                                                                                                      ",
        "PPPPPPPPPPPPPP3      22                                    pppppppppppppppppppppppppp                                        ",
        "666666666666666      22                                                                                                      ",
        "                     22                                                                                                      ",
        "                     22PPPPPPPPPPPPPPPPPPPPPPPPPPPP1                                                                         ",
        "          31    G    2222222666666666666666666222222                                                                         ",
        "          22    G    2222666                  666666                                                                         ",
        "GG        22    G    2226                                                                                                    ",
        "P1        22    G    226  Q                                                                                                  ",
        "66        22    G    22                                                                                                      ",
        "          22    G    22                                                                                                      ",
        "        GG22    G    22                                                                                                      ",
        "        3P22         22                                                                                                      ",
        "        6622         22                        3PPPPPPPPPPP1             3PPPPPPPPPPPP1                                      ",
        "          22         22                     Q  2222222226666             22222222222222                                      ",
        " G        22         22           3PPPPPPPPPPPP222226666                                                                     ",
        "P1        22         22            66666222222222226                                                                         ",
        "66        22    G    22PPP1             66622222222                                                                          ",
        "          22    G    2222221               666622221                                                                         ",
        "        GG22    G    2222222P1                 22222                                                                         ",
        "        3P22         22                3PPPPP2222222PP1                                                                      ",
        "        6622         22                6666666222222222PPP1                                                                  ",
        "   F      22                     1            2222222222222PPPPPP                                                            ",
        "PPPPPPPPPP22                    32            G222222222222222222                                                            ",
        "222222222222         3PPPPPPPPPP22     PPPPP222222222222222222222                                                            ",
        "222222222222         2222222222222     66622222222222222222222222                                                            ",
        "222222222222         2222222222222        22222222222222222222222                                                            "]



    level = [
        " S S S S  S          22                                                                     ",
        "PPPPPPPPPPPPPP3      22                                    PPPPPPPPPPPPPPPPPPPPPPPPPPP      ",
        "666666666666666      22                                                                     ",
        "                     22                                                                     ",
        "                     22PPPPPPPPPPPPPPPPPPPPPPPPPPPP1                                        ",
        "          31    G    2222222666666666666666666222222                                        ",
        "          22    G    2222666                  666666                                        ",
        "GG        22    G    2226                                                                   ",
        "P1        22    G    226  Q                                                                 ",
        "66        22    G    22                                                     Q               ",
        "          22    G    22                                                                     ",
        "        GG22    G    22                                                                     ",
        "        3P22         22                                                                     ",
        "        6622         22                        3PPPPPPPPPPP1       3PPPPPPPPPPPP1           ",
        "          22         22                     Q  2222222226666       22222222222222           ",
        " G        22         22           3PPPPPPPPPPPP222226666       G        2222222222 GGGGGG   ",
        "P1        22         22            66666222222222226           G      M   2222222222 GGGGGGG",
        "66        22    G    22PPP1             66622222222   M        G     PPPPP22222222222GGGGGGG ",
        "          22    G    2222221               66662222PPPPPP1       PPPPP2222222222222222PPPPPPP",
        "        GG22    G    2222222P1                 2222266666      22222222222222222222222222    ",
        "        3P22         22                3PPPPP222222 GGG        666666666622222222222222      ",
        "        6622         22                6666222222222222PPP1  GG            M 22222222222     ",
        "   F      22                     1         666222222222222PPPPPP           22222222222222222 ",
        "PPPPPPPPPP22                    32            G2222222222222226     2222222222222222222222222",
        "222222222222         3PPPPPPPPPP22     PPPPP222222222222266666          222          222   E ",
        "222222222222         2222222222222     666222222222222222 Q      31 GGG         31        PPP",
        "222222222222         2222222222222        222222222222222222    322PPPPPPP1    322PPPPPPPP222"]

    level_vacio = [
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             "]

    player_settings = (32, 32,PATH+ "froggy.png")


    level = Level(level, player_settings, PATH+'bg_music1.ogg')


    done = play_again = False
    while not (done or play_again):
        timer.tick(60)


        for e in pygame.event.get():
            if e.type == QUIT:
                done = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                paused = True#change for paused menu
                pause()
                up = down = left = right = space = running = False
                pygame.event.clear()
                break
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                space = True
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

class EnemyMosquito(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.vida=1
        self.xvel = 4.0
        self.yvel = 4.0
        self.follow = False
        self.onGround = False
        self._image_origin = pygame.image.load(PATH + "mosquito1.png")
        self._image_origin = pygame.transform.scale(self._image_origin, (32, 32)).convert_alpha()
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
        self.image = self._image_origin
        image_rect = (self.image.get_rect().size)
        self.image.convert()
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
        self.disparado = False
    def update(self, platforms, enemies, entities, posX, posY, level_width, level_high):
        if(not self.disparado):
            self.xvel = 4.0
            self.yvel = 4.0
            self.move_towards_player(posX, posY)
            self.collide(self.xvel, 0, platforms)
            self.collide(0, self.yvel, platforms)
        else:
            self.rect.x += self.xvel
            self.collide_anything(platforms, enemies, entities)
        if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width):
            self.perdervida(enemies, entities)
    def move_towards_player(self, posX, posY):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.rect.x - posX, self.rect.y - posY
        dist = math.hypot(dx, dy) #math.sqrt(dx*dx + dy*dy)
        if not self.follow:
            if dist < 400:
                self.follow = True
            else:
                return
        try:
            dx, dy = dx * -1.0 / dist, dy * -1.0 / dist
        except ZeroDivisionError:
            print("Divided by zero")
        # move along this normalized vector towards the player at current speed
        self.xvel, self.yvel = dx * self.xvel, dy * self.yvel
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if dx > 0:
            self.image = self._image_toLeft
        else:
            self.image = self._image_origin

    def observar(self, posX, posY, platforms, enemies, entities,  level_width, level_high):
        self.update(platforms, enemies, entities, posX, posY, level_width, level_high)
        pass

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if abs(self.rect.right - p.rect.left) < abs(self.xvel) + 1:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    print("Enemy collide right")
                if abs(self.rect.left - p.rect.right) < abs(self.xvel) + 1:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    print("Enemy collide left")
                if abs(self.rect.bottom - p.rect.top) < abs(self.yvel) + 1:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                if abs(self.rect.top - p.rect.bottom) < abs(self.yvel) + 1:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print("Enemy collide top")

    def salir_disparado(self, dir):
        print("salidisparado")
        self.disparado = True
        if dir == 'derecha':
            self.xvel = 12.0
        else:
            self.xvel = -12.0

    def collide_anything(self, platforms, enemies, entities):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.disparado = False
                self.xvel = 0
                self.perdervida(enemies, entities)
                return
        for e in enemies:
            if e != self and pygame.sprite.collide_rect(self, e):
                self.disparado = False
                self.xvel = 0
                if isinstance(e, EnemySpider):
                	e.perdervida(enemies, entities)
                if isinstance(e, EnemyMosquito):
                	e.perdervida(enemies, entities)
                self.perdervida(enemies, entities)
                return

    def perdervida(self, enemies, entities):
        self.vida = self.vida - 1
        if self.vida < 1: #morir
            enemies.remove(self)
            entities.remove(self)
            self = None

class EnemySpider(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.vida = 1
        self.xvel = 4.0
        self.yvel = 4.0
        self.follow = False
        self.onGround = False
        self._image_origin = pygame.image.load(PATH + "spider1.png")
        self._image_origin = pygame.transform.scale(self._image_origin, (32, 32)).convert_alpha()
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
        self.image  = self._image_origin
        image_rect = (self.image.get_rect().size)
        self.image.convert()
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
    def update(self, platforms, enemies, entities, posX, posY, level_width, level_high):
        self.xvel = 3.0
        self.yvel = 4.0
        self.move_towards_player(posX, posY)
        self.collide(self.xvel, 0, platforms)
        self.collide(0, self.yvel, platforms)
        if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width):
            self.perdervida(enemies, entities)

    def move_towards_player(self, posX, posY):
        dist = math.hypot(self.rect.x - posX, self.rect.y - posY) #math.sqrt(dx*dx + dy*dy)
        if not self.follow:
            if dist < 200:
                self.follow = True
            else:
                return
        dx = posX - self.rect.x
        self.rect.y += 4.0
        if abs(self.rect.x - posX)>3:
            if dx > 0:
                self.image = self._image_toLeft
                self.rect.x +=self.xvel
            elif dx < 0:
                self.image = self._image_origin
                self.rect.x -=self.xvel

    def observar(self, posX, posY, platforms, enemies, entities,  level_width, level_high):
        self.update(platforms, enemies, entities, posX, posY, level_width, level_high)
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if abs(self.rect.right - p.rect.left) < abs(self.xvel)+1 and self.overlap((self.rect.top, self.rect.bottom),(p.rect.top, p.rect.bottom)):
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    print ("Enemy collide right")
                if abs(self.rect.left - p.rect.right) < abs(self.xvel)+1 and self.overlap((self.rect.top, self.rect.bottom),(p.rect.top, p.rect.bottom)):
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    print ("Enemy collide left")
                if abs(self.rect.bottom - p.rect.top) < abs(self.yvel)+1:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                if abs(self.rect.top - p.rect.bottom) < abs(self.yvel)+1:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print ("Enemy collide top")
    def overlap(self, t1,t2):
        return t1[0]<=t2[1] and t2[0]<=t1[0]
    def perdervida(self, enemies, entities):
        self.vida = self.vida - 1
        if self.vida < 1: #morir
            enemies.remove(self)
            entities.remove(self)
            self = None

class Player(Entity):
    def __init__(self, x, y, image_path):
        Entity.__init__(self)
        self.counter=0
        self.counter_lengua=0
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self._image_origin = pygame.image.load(PATH +"sprite_froggy0.png")
        self._image_origin = pygame.transform.scale(self._image_origin, (52, 52)).convert_alpha()
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
        self.image  = self._image_origin

        image_rect = (32,32)#(self.image.get_rect().size)
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
        self.tongue = 0

        self.enemy_get = None


        #todas las demas imagenes
        path_tongue = "froggy_tongue/"
        path_walk = "froggy_walk/"

        self.imagenes_derecha = []
        self.imagenes_izquierda = []

        self.imagenes_walk_derecha = []
        self.imagenes_walk_izquierda = []

        self.imagenes_derecha.append(self._image_origin)
        self.imagenes_izquierda.append(self._image_toLeft)
        for i in range(4):# lengua
            i=i+1
            im = pygame.image.load(PATH+ path_tongue+"froggy_tongue_"+str(i)+".png")
            im = pygame.transform.scale(im, (52, 52)).convert_alpha()
            self.imagenes_derecha.append(im)
            im_toLeft = pygame.transform.flip(im, True, False).convert_alpha()
            self.imagenes_izquierda.append(im_toLeft)

        self.imagenes_walk_derecha.append(self._image_origin)
        self.imagenes_walk_izquierda.append(self._image_toLeft)
        for i in range(2): #walk
            i=i+1
            im = pygame.image.load(PATH+ path_walk+"sprite_froggy"+str(i)+".png")
            im = pygame.transform.scale(im, (52, 52)).convert_alpha()
            self.imagenes_walk_derecha.append(im)
            im_toLeft = pygame.transform.flip(im, True, False).convert_alpha()
            self.imagenes_walk_izquierda.append(im_toLeft)


        self.lado = 'derecha'
        self.animacion = Animacion()
        self.agarrado = False
        self.espera = 0

        ############################################################################
        self.puntaje = 0


        ################
        self.forma = [0, 'ida']

        self.forma_walk = [0, 'ida']
        self.sacandolengua=False
    def update(self, up, down, left, right, space, running, platforms, enemies, entities, gemas, level_width, level_high):
        vida = True
        if up:
            # only jump if on the ground
            if self.onGround:
                self.yvel -= 9
                try:
                    jumpsound= pygame.mixer.Sound(PATH+'sounds/Froggy_Jump.wav')
                    jumpsound.play()
                except Exception:
                    print("no audio")
        if down:
            pass
        #if running:
            #self.xvel = 12
        if not self.sacandolengua:
	        if left:
	            self.xvel = -6.3
	            self.lado = 'izquierda'
	        if right:
	            self.xvel = 6.3
	            self.lado = 'derecha'
        '''if space:
        	if self.enemy_get is not None:
	            self.enemy_get.rect.x=self.rect.x
	            self.enemy_get.rect.y=self.rect.y
	            self.enemy_get.salir_disparado(self.lado)
	            self.enemy_get = None
        	if self.tongue <= 0:
	            self.tongue = 100'''
        #print(self.tongue)
        #self.enemy_get.update(platforms, 0, 0)
        #self.screen.blit(self.enemy_get.image, ())

        #franco
        if self.agarrado == True:
            self.espera = self.espera + 1

            if self.espera >= 10:
                ########### aca no estoy seguro... antes estaba solo espacio y por eso siempre se lanzaba el insecto aunque no lo tengas
                    ####### ahora puse que tenga que tenerlo
                if space== True:
                    print('xxxxxxxxxxxxxxxxxx')
                    entities.add(self.enemy_get)
                    self.enemy_get.rect.x=self.rect.x
                    self.enemy_get.rect.y=self.rect.y
                    self.enemy_get.salir_disparado(self.lado)
                    self.espera = 0
                    self.agarrado = False
                    if self.tongue <= 0:
                        self.tongue = 100
                    #print(self.tongue)
                    #self.enemy_get.update(platforms, 0, 0)
                    #setlf.screen.blit(self.enemy_get.image, ())

        if self.espera < 15 and self.agarrado == False:
            self.espera = self.espera + 1

        if space and self.sacandolengua==False:
            self.sacandolengua = True
        if self.sacandolengua == True:
	        #cambiar imagen
	        self.sacarlengua(self.lado)
	        if abs(self.xvel) > 0.2:
	        	self.xvel =  self.xvel - numpy.sign(self.xvel)*0.1
	        else:
	        	self.xvel = 0

        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100:
            	self.yvel = 100
        if not(left or right):
            self.xvel = 0
            self.forma_walk = [0, 'ida']
            if self.sacandolengua == False:
            	if self.lado == 'izquierda':
	                self.image = self.imagenes_walk_izquierda[self.forma_walk[0]]
            	else:
	                self.image = self.imagenes_walk_derecha[self.forma_walk[0]]
        elif self.sacandolengua == False:
            self.walkloop(self.lado)
            if self.lado == 'izquierda':
                self.image = self.imagenes_walk_izquierda[self.forma_walk[0]]
            else:
                self.image = self.imagenes_walk_derecha[self.forma_walk[0]]
        if (self.tongue >= 0):
            self.tongue -= 1
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
        vida = self.collide_enemies(enemies, entities)
        self.beobserver(enemies, platforms, entities,  level_width, level_high)
        #############################################################################################
        self.collide_gemas(gemas, entities)
        print('puntaje')
        print(self.puntaje)
        #############################################################################################

        if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width or (vida)):
            return False
        else:
            return True

    def sacarlengua(self, dir):
        self.counter_lengua = self.counter_lengua + 1
        if self.counter_lengua > 40:
            self.counter_lengua = 0
            self.sacandolengua = False
            self.forma = [0, 'ida']
        elif self.counter_lengua % 5 == 0:
            print(self.counter_lengua)
            if dir == 'derecha':
                self.forma = self.animacion.animarCompleta(self.imagenes_derecha, self.forma)
                self.image = self.imagenes_derecha[self.forma[0]]
            else:
                self.forma = self.animacion.animarCompleta(self.imagenes_izquierda, self.forma)
                self.image = self.imagenes_izquierda[self.forma[0]]

    def walkloop(self, dir):
        self.counter = self.counter + 1
        if self.counter > 50:
            self.counter = 0
        elif self.counter % 10 == 0:
            print(self.counter)
            if dir == 'derecha':
                self.forma_walk = self.animacion.animarCompleta(self.imagenes_walk_derecha, self.forma_walk)
                self.image = self.imagenes_walk_derecha[self.forma_walk[0]]
            else:
                self.forma_walk = self.animacion.animarCompleta(self.imagenes_walk_izquierda, self.forma_walk)
                self.image = self.imagenes_walk_izquierda[self.forma_walk[0]]

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print("collide top")

    '''def collide_enemies(self, enemies, entities):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                if isinstance(e, EnemyMosquito):
                    if e.disparado:
                        return False
                print("--------CHOCA------")
                return True
        return False'''
    def collide_enemies(self, enemies, entities):
        for e in enemies:
            if isinstance(e, EnemyMosquito) and self.agarrado == False and self.forma[0] != 0 and self.espera == 15:
                self.agarrado = self.agarrarObjeto(e)


                if self.agarrado == True:
                    self.enemy_get = e
                    entities.remove(e)

            # este es para que el enemigo tragado no le haga perder vida
            if e == self.enemy_get:
                pass

            # aca es para todos los demas enemigos
            elif pygame.sprite.collide_rect(self, e):
                return True
        return False

    #############################################################################################
    def collide_gemas(self, gemas, entities):
        for e in gemas:
            cogio_gema = False

            cogio_gema = self.agarrarObjeto(e)

            if(cogio_gema == True):
                self.puntaje = self.puntaje + e.valor
                entities.remove(e)
                gemas.remove(e)

        return False
    #############################################################################################

    def beobserver(self, enemies, platforms, entities, level_width, level_high):
        for q in enemies:
            if isinstance(q, EnemyMosquito):
                q.observar(self.rect.x, self.rect.y, platforms, enemies, entities, level_width, level_high)
            else:
                q.observar(self.rect.x, self.rect.y, platforms, enemies, entities, level_width, level_high)


    def agarrarObjeto(self, objeto):
        agarro = False
        """
        if self.lado == 'izquierda':

            if self.rect[0]>= objeto.rect[0] and self.rect[0] <= objeto.rect[0] + objeto.rect[2]:
                # se usara el punto medio en el eje Y de froggy: self.rect[1] + self.rect[3]/2
                if self.rect[1] + self.rect[3]/2 >= objeto.rect[1] and self.rect[1] + self.rect[3]/2 <= objeto.rect[1] + objeto.rect[3]:
                    agarro = True
        else:

            if self.rect[0] + self.rect[2] >= objeto.rect[0] and self.rect[0] + self.rect[2] <= objeto.rect[0] + objeto.rect[2]:
                if self.rect[1] + self.rect[3]/2 >= objeto.rect[1] and self.rect[1] + self.rect[3]/2 <= objeto.rect[1] + objeto.rect[3]:
                    agarro = True
        """

        #return agarro
        return pygame.sprite.collide_rect(self, objeto)


def crop(image_name, rx, ry):
        pil_image = Image.open(image_name)
        size = (pil_image.width, pil_image.height)
        np_array = numpy.array(pil_image)
        blank_px = [255, 255, 255, 0]
        mask = np_array != blank_px
        coords = numpy.argwhere(mask)
        try:
            x0, y0, z0 = coords.min(axis=0)
            x1, y1, z1 = coords.max(axis=0) + 1
            cropped_box = np_array[x0:x1, y0:y1, z0:z1]
            pil_image = Image.fromarray(cropped_box, 'RGBA')
        except Exception:
            pass
        print(image_name + str((pil_image.width, pil_image.height)))
        return (pil_image.width * rx / size[0], pil_image.height * ry / size[1])


class Platform(Entity):
    def __init__(self, x, y, image_path):
        Entity.__init__(self)

        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
            self.image = IMAGES[(PATH + image_path, 32, 32)]
        except KeyError:
            image_rect = crop(PATH + image_path, 32, 32)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path, 32, 32) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (32, 32)).convert_alpha()
                IMAGES[(PATH + image_path, 32, 32)] = self.image
        self.rect = Rect(x, y, image_rect[0], image_rect[1])

    def update(self):
        pass


class Decoration(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        self._image_origin = pygame.image.load(PATH + image_path)
        self._image_origin = pygame.transform.scale(self._image_origin, (w, h))
        self.image = self._image_origin
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
        self.rect = Rect(x, y - h + 32, image_rect[0], image_rect[1])

    def update(self):
        pass

#############################################################################################
class Gemas(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        self._image_origin = pygame.image.load(PATH + image_path)
        self._image_origin = pygame.transform.scale(self._image_origin, (w, h))
        self.image = self._image_origin
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
        self.rect = Rect(x, y - h + 32, image_rect[0], image_rect[1])

        self.valor = 20

    def update(self):
        pass
#############################################################################################

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y, "platform/18.png")


class Animacion:
    def __init__(self):
        pass

    def animarCompleta(self, imagenes, forma):
        # es +1 ya que en la ultima posicion va a ir si es ida o vuelta
        if forma[0] + 1 == len(imagenes):
            forma[1] = 'vuelta'
        # se verifica si esta en la ida o vuelta
        if forma[1] == 'ida':
            forma[0] = forma[0] + 1
        elif forma[1] == 'vuelta':
            forma[0] = forma[0] - 1
            if forma[0] == 0:
                forma[1] = 'ida'
        return forma

    def animarIda(self, imagenes, i):

        # es +1 ya que aca no hay ida o vuelta
        if i + 1 == len(imagenes):
            i = 0
        else:
            i = i + 1
        return i


if __name__ == "__main__":
    main()
