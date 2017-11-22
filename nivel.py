
from pygame import *
from constantes import *
from objetosestaticos import *
from seresvivos import *
from pantallas import GameMenu

import json



class Partida():
    def __init__(self):
        #para cambiar niveles cambiar el nombre a level (no duplicados)


        self.player_settings = (32, 32, PATH + "froggy.png")

        self.niveles_data = Conexion().listar_niveles()

    def mostrar_pantalla_niveles(self):

        niveles_funciones = {}
        def function_builder(id, bg_music, bg_image):
            def function(param):
                param.mainloop=False
                self.cargar_nivel(id, self.player_settings, bg_music, bg_image)
            return function
        for element in self.niveles_data:
            bg_music = element["bg_music"]
            bg_image = element["bg_image"]
            def load_level(param):
                param.mainloop=False
                self.cargar_nivel(element["id"], self.player_settings, PATH + bg_music, PATH + bg_image)
            niveles_funciones[element["title"]] = function_builder(element["id"], PATH + bg_music, PATH + bg_image)

        def mini_function(param):
            param.mainloop=False
        niveles_funciones["Pantalla principal"] = mini_function

        screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
        '''
        menu_items = ('Iniciar', 'Mostrar Creditos', 'Salir')
        funcs = {'Iniciar': iniciar,
                 'Mostrar Creditos' : mostrar_creditos,
                 'Salir': sys.exit}
        '''

        pygame.display.set_caption("Froggy!")
        timer = pygame.time.Clock()
        gm = GameMenu(screen, niveles_funciones.keys(), niveles_funciones)
        gm.run()

    def pause(self):
        pygame.event.clear()
        while True:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    return

    def cargar_nivel(self, id_nivel, player_settings, bg_music, bg_image):

        up = down = left = right = space = running = False
        level = Level(id_nivel, player_settings, bg_music, bg_image) #player_settings, PATH+'bg_music1.ogg')
        done = play_again = False
        timer = pygame.time.Clock()
        while not (done or play_again):
            timer.tick(FPS_RATE)
            for e in pygame.event.get():
                if e.type == QUIT:
                    done = True
                    pygame.quit()
                    import sys
                    sys.exit
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    paused = True#change for paused menu
                    self.pause()
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
            #self.cargar_nivel(id_nivel, player_settings, bg_music, bg_image)
            pass
        else:
            pygame.quit()
            import sys
            sys.exit


class Level():
    def __init__(self, id_nivel, player_settings, bg_music, bg_image):
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.bg = pygame.Surface((32,32))
        self.bg.convert()
        self.entities = pygame.sprite.Group()
        self.player_settings = player_settings
        self.platforms = []
        self.decorations = []
        self.enemies = []
        ########################################################nuevo
        self.gemas = []
        self.corazon = []
        ########################################################


        self.escenarios = [] # lista de mapas de nivel
        escenarios = [] # lista de mapas de nivel
        data = Conexion().listar_escenarios(id_nivel)
        from constantes import PATH
        for element in data:
            with open(PATH+element["mapa"]) as json_file:
                data_map=json.load(json_file)
                self.escenarios.append(data_map)
        self.escenario_index = 0
        self.level = self.escenarios[self.escenario_index] #inicializar en uno
        # build the level

        self.total_level_width, self.total_level_height = 0 , 0
        self.construir_mapa(self.level, self.player_settings)


        #self.camera = Camera(Camera.complex_camera, self.total_level_width, self.total_level_height)
        #self.entities.add(self.player)

        self.backGround = Background(bg_image, [0,0], (WIN_WIDTH, WIN_HEIGHT))
        try:
            self.playmusic(bg_music)
        except Exception:
            print("no bg music")

        ####################################################################################################

        self.vidas_inicio = FROGGY_VIDA
        self.letra_datos = 20
        self.datos = Datos_partida("items/gem_9.png", "items/corazon.jpg",self.letra_datos, self.vidas_inicio)
        ####################################################################################################

    def construir_mapa(self, level, player_settings):
        x = y = 0
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

    def update(self, up, down, left, right, space, running):
        # draw background
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))

        self.camera.update(self.player)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.backGround.image, self.backGround.rect)
        # update player, draw everything else
        if self.player.onExitBlock:
            #wea de apasar nivel
            self.escenario_index += 1
            if self.escenario_index < len(self.escenarios):
                print("construido")
                self.entities = pygame.sprite.Group()
                self.platforms = []
                self.decorations = []
                self.enemies = []
                self.gemas = []
                self.corazon = []

                self.construir_mapa(self.escenarios[self.escenario_index],self.player_settings)
                return;
            else:
                print("Ganasteeeeee")
                return False
        if not self.player.update(up, down, left, right, space, running, self.platforms, self.enemies, self.entities,self.gemas, self.corazon, self.datos, self.total_level_width, self.total_level_height):
            return False
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
        '''
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
        '''
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


    def construir(self, x, y, player_settings, col):
        '''
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

        if col == "W":
            w = EnemyBoss(x, y)
            self.enemies.append(w)
            self.entities.add(w)

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
        '''
        dict_my_data = {
            "1": {"image":"jungle_pack_07.png", "type": Platform},
            "2": {"image":"jungle_pack_35.png", "type": Platform},
            "P": {"image":"jungle_pack_05.png", "type": Platform},
            "3": {"image":"jungle_pack_03.png", "type": Platform},
            "4": {"image":"jungle_pack_11.png", "type": Platform},
            "5": {"image":"jungle_pack_19.png", "type": Platform},
            "6": {"image":"jungle_pack_21.png", "type": Platform},
            "7": {"image":"jungle_pack_40.png", "type": Platform},
            "0": {"image":"jungle_pack_09.png", "type": Platform},

            "E": {"type": ExitBlock},


            "Q": {"type": EnemyMosquito},
            "S": {"type": EnemySpider},
            "W": {"type": EnemyBoss},


            "D": {"image":"jungle_pack_67.png", "type": Decoration, "w":128, "h":128},
            "!": {"image":"jungle_pack_59.png", "type": Decoration, "w":128, "h":128},
            "¡": {"image":"jungle_pack_57.png", "type": Decoration, "w":128, "h":128},
            "B": {"image":"jungle_pack_66.png", "type": Decoration, "w":128, "h":128},


            "G": {"image":"gem_9.png", "type": Gemas, "w":16, "h":16},
            "C": {"image":"vida.png", "type": Corazon, "w":32, "h":32},

            "F": {"type": Player},
            " ": {"type": None}
        }
        element = None
        PLATFORM_PATH = "platform/"
        ITEM_PATH = "items/"
        try:
            obj_sprite = dict_my_data[col]
            if obj_sprite["type"] == Player:
                self.player = Player(x, y, player_settings[2])
            elif obj_sprite["type"] == Decoration:
                element =  Decoration(x, y, obj_sprite["w"], obj_sprite["h"], PLATFORM_PATH + obj_sprite["image"])
                self.decorations.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == Platform:
                element = Platform(x, y, PLATFORM_PATH + obj_sprite["image"])
                self.platforms.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == ExitBlock:
                element = ExitBlock(x, y)
                self.platforms.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == EnemyMosquito:
                element = EnemyMosquito(x, y)
                self.enemies.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == EnemySpider:
                element = EnemySpider(x, y)
                self.enemies.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == Gemas:
                element = Gemas(x, y, obj_sprite["w"], obj_sprite["h"], ITEM_PATH + obj_sprite["image"])
                self.gemas.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == Corazon:
                element = Corazon(x, y, obj_sprite["w"], obj_sprite["h"], ITEM_PATH + obj_sprite["image"])
                self.corazon.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == EnemyBoss:
                element = EnemyBoss(x, y)
                self.enemies.append(element)
                self.entities.add(element)
            elif obj_sprite["type"] == None:
                pass
            else:
                print("no se encontro: " + obj_sprite["type"].__name__)
        except Exception as e:
            raise e




class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, screen_sizes):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, screen_sizes).convert_alpha()
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
        self._image_gema = pygame.transform.scale(self._image_gema, (self.datos[0].get_rect()[3], self.datos[0].get_rect()[3])).convert_alpha()
        self.datos.append( self._image_gema )

        # VIDAS INICIO
        self.datos.append( self.letra.render(str(vidas_inicio), True, (100,200,0), None ))

        # IMAGEN VIDA
        self._image_vida = pygame.image.load(PATH + image_path_vida)
        self._image_vida = pygame.transform.scale(self._image_vida, (self.datos[0].get_rect()[3], self.datos[0].get_rect()[3])).convert_alpha()
        self.datos.append( self._image_vida )

        #self.screen.blit(imagenTextoPresent, (400, 10))
        #self.screen.blit(imagenTextoPresent, (400 + imagenTextoPresent.get_rect()[2], 10))


    def update(self):
        self.datos[0] = self.letra.render(str(self.puntaje), True, (100,200,0), None )
        self.datos[2] = self.letra.render(str(self.vidas_restantes), True, (100,200,0), None )
