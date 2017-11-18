
from pygame import *
from constantes import *
from objetosestaticos import *
from seresvivos import *

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

        self.corazon = []
        ########################################################
        x = y = 0
        self.level = level
        # build the level

        for row in level:
            for col in row:
                self.construir(x, y, player_settings, col)
                x += 32
            y += 32
            x = 0
        self.total_level_width  = len(level[0])*32
        self.total_level_height = len(level)*32

        self.camera = Camera(Camera.complex_camera, self.total_level_width, self.total_level_height)
        self.entities.add(self.player)

        self.backGround = Background(PATH+'platform/bg_jungle.png', [0,0], (800, 640))
        try:
            self.playmusic(bg_music)
        except Exception:
            print("no bg music")

        ####################################################################################################
        self.vidas_inicio = 3
        self.letra_datos = 20
        self.datos = Datos_partida("items/gem_9.png", "items/corazon.jpg",self.letra_datos, self.vidas_inicio)
        ####################################################################################################

    def construir(self, x, y, player_settings, col):
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



            #CORAZON
        if col == "C":
            c = Corazon(x, y, 32,32, "items/vida.png")
            self.corazon.append(c)
            self.entities.add(c)



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

    def update(self, up, down, left, right, space, running):
        # draw background
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))

        self.camera.update(self.player)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.backGround.image, self.backGround.rect)
        # update player, draw everything else
        if not self.player.update(up, down, left, right, space, running, self.platforms, self.enemies, self.entities,self.gemas, self.corazon, self.datos, self.total_level_width, self.total_level_height):
            return False
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

        ####################################################################################################
        self.datos.update()
        self.mostrarDatos()

    def mostrarDatos(self):
        ancho = 0

        for d in self.datos.datos:
            self.screen.blit(d, (400 + ancho,10))
            ancho =  ancho + d.get_rect()[2] + 5
        ####################################################################################################

    def playmusic(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1, 0.0)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, screen_sizes):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, screen_sizes)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Datos_partida():
    def __init__(self, image_path_gema, image_path_vida, letra_datos, vidas_inicio):
        self.puntaje = 0
        self.vidas_restantes = vidas_inicio
        self.datos = []

        # PUNTAJE
        self.letra = pygame.font.SysFont("Arial", letra_datos)
        self.datos.append( self.letra.render(str(self.puntaje), True, (100,200,0), None ))

        # IMAGEN GEMA
        self._image_gema = pygame.image.load(PATH + image_path_gema)
        self._image_gema = pygame.transform.scale(self._image_gema, (self.datos[0].get_rect()[3], self.datos[0].get_rect()[3]))
        self.datos.append( self._image_gema )

        # VIDAS INICIO
        self.datos.append( self.letra.render(str(vidas_inicio), True, (100,200,0), None ))

        # IMAGEN VIDA
        self._image_vida = pygame.image.load(PATH + image_path_vida)
        self._image_vida = pygame.transform.scale(self._image_vida, (self.datos[0].get_rect()[3], self.datos[0].get_rect()[3]))
        self.datos.append( self._image_vida )

        #self.screen.blit(imagenTextoPresent, (400, 10))
        #self.screen.blit(imagenTextoPresent, (400 + imagenTextoPresent.get_rect()[2], 10))


    def update(self):
        self.datos[0] = self.letra.render(str(self.puntaje), True, (100,200,0), None )
        self.datos[2] = self.letra.render(str(self.vidas_restantes), True, (100,200,0), None )
