import pygame as pg
import random
from settings import *
from sprites import *
import copy

class Game:

    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name=pg.font.match_font(FONT_NAME)

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()

        self.platforms = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p= Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        #si el jugador va hacia la derecha - centrar jugador
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            if self.player.rect.right >= WIDTH / 2:
                for plat in self. platforms:
                    plat.rect.x -= abs(self.player.vel.x)
                self.player.pos.x -= abs(self.player.vel.x)

                # Si nos caemomos del mapa GAME over
        if self.player.rect.bottom > HEIGHT:
            self.playing = False

        #cuando el juegdor cae sobre plataforma
        if self.player.vel.y>0:
            for plat in self. platforms:
                col = pg.sprite.collide_rect(self.player, plat)
                if col == True:
                    self.player.pos.y = plat.rect.top+1
                    self.player.vel.y = 0
            #nigga=copy.copy(self.platforms)
            #hits = pg.sprite.spritecollide(self.player, nigga, False)
            #if hits:
            #    self.player.pos.y = hits[0].rect.top+1
            #    self.player.vel.y = 0
            #    if keys[pg.K_RIGHT]:
            #        hits[0].rect.x -= abs(self.player.vel.x)


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(LIGHTBLUE)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        imagen1 = pg.image.load("img/logo.png")
        imagen1 =pg.transform.scale(imagen1,(550,200))

        self.screen.fill(LIGHTBLUE)
        self.screen.blit(imagen1,(WIDTH/4,HEIGHT/4))
        self.draw_text("PRESS ANY KEY",32,BLACK,WIDTH/2,HEIGHT*3 /4)

        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        pass


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
