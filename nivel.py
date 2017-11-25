
import pygame
from constantes import *
from objetosestaticos import *
from seresvivos import *
from pantallas import GameMenu, Datos_partida

import json




class Partida():
    def __init__(self, screen):
        #para cambiar niveles cambiar el nombre a level (no duplicados)
        self.screen = screen

        self.player_settings = (32, 32, PATH + "froggy.png")

        self.niveles_data = Conexion().listar_niveles()

    def mostrar_pantalla_niveles(self):

        screen = self.screen
        niveles_funciones = {}
        def function_builder(id, bg_music, bg_image, screen):
            def function(param):
                param.mainloop=False
                self.cargar_nivel(id, self.player_settings, bg_music, bg_image, screen)
            return function
        for element in self.niveles_data:
            bg_music = element["bg_music"]
            bg_image = element["bg_image"]
            def load_level(param):
                param.mainloop=False
                self.cargar_nivel(element["id"], self.player_settings, bg_music, bg_image, screen)
            niveles_funciones[element["title"]] = function_builder(element["id"], bg_music, bg_image, screen)

        def mini_function(param):
            param.mainloop=False
        niveles_funciones["Pantalla principal"] = mini_function

        pygame.display.set_caption("Froggy!")
        timer = pygame.time.Clock()
        gm = GameMenu(screen, niveles_funciones.keys(), niveles_funciones)
        gm.run()

    def cargar_nivel(self, id_nivel, player_settings, bg_music, bg_image, screen):

        
        level = Level(id_nivel, player_settings, bg_music, bg_image, screen) #player_settings, PATH+'bg_music1.ogg')
        done = play_again = False
        timer = pygame.time.Clock()
        while not (done or play_again):
            timer.tick(FPS_RATE)
            if(level.update()==False):
                play_again = True
            pygame.display.update()
        if(play_again):
            #self.cargar_nivel(id_nivel, player_settings, bg_music, bg_image)
            pass
        else:
            pygame.quit()
            exit()


class Level():
    def __init__(self, id_nivel, player_settings, bg_music, bg_image, screen):
        self.screen = screen
        self.bg = pygame.Surface((32,32))
        self.bg.convert()
        self.entities = pygame.sprite.Group()
        self.player_settings = player_settings
        self.platforms = []
        self.decorations = []
        self.enemies = []
        self.gemas = []
        self.corazon = []
        self.feather= []

        self.escenarios = [] # lista de mapas de nivel
        self.up = self.down = self.left = self.right = self.space = self.running = False

        escenarios = [] # lista de mapas de nivel
        data = Conexion().listar_escenarios(id_nivel)

        #from constantes import PATH
        data_map = None

        for element in data:
            '''if REST_MODE:
                data_map = requests.get(element["mapa"]).json()
            else:
                with open(element["mapa"]) as json_file:
                    data_map = json.load(json_file)'''
            data_map = load_manager(element["mapa"], isJson=True)
            #data_map = json.load(load_manager(element["mapa"]))
            self.escenarios.append((element["id"], data_map))
        self.escenario_index = 0
        self.level = self.escenarios[self.escenario_index] #inicializar en uno

        # build the level

        self.total_level_width, self.total_level_height = 0 , 0
        self.construir_mapa(self.level, self.player_settings)



        bg_image = load_manager(bg_image)
        bg_music = load_manager(bg_music)

        self.backGround = Background(bg_image, [0,0], (WIN_WIDTH, WIN_HEIGHT))
        try:
            self.playmusic(bg_music)
        except Exception:
            print("no bg music")

        ####################################################################################################

        self.vidas_inicio = FROGGY_VIDA
        self.letra_datos = 20
        self.datos = Datos_partida("items/gem_9.png", "items/vida.png","items/feather.png",self.letra_datos, self.vidas_inicio)
        ####################################################################################################

    def construir_mapa(self, level, player_settings):
        self.mostrar_historia(level[0], 'A')
        x = y = 0
        mapa = level[1]
        for row in mapa:
            for col in row:
                self.construir(x, y, player_settings, col)
                x += 32
            y += 32
            x = 0
        self.total_level_width  = len(mapa[0])*32
        self.total_level_height = len(mapa)*32

        self.camera = Camera(Camera.complex_camera, self.total_level_width, self.total_level_height)
        self.entities.add(self.player)

    def mostrar_historia(self, escenario_id, modalidad):
        self.up = self.down = self.left = self.right = self.space = self.running = False
        pygame.event.pump()
        pygame.event.clear()
        data = Conexion().listar_historia(escenario_id, modalidad)
        screen = self.screen
        bg_color = BLACK
        screen.fill(bg_color)
        sig_imagen = True
        for element in data:
            if sig_imagen:
                image = pygame.image.load(load_manager(element["imagen"]))#PATH+element["imagen"])
                image = pygame.transform.scale(image,(WIN_WIDTH,WIN_HEIGHT)).convert_alpha()
                image_width, image_height= image.get_size()
                screen.blit(image, ((WIN_WIDTH-image_width)/100, (WIN_HEIGHT-image_height)/100))
                sig_imagen = False
            pygame.display.flip()
            while not sig_imagen:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                        sig_imagen = True
    def pause(self):
        #pygame.event.clear()
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return
    def listenKey(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.pause()
                self.up = self.down = self.left = self.right = self.space = self.running = False
                #pygame.event.clear()
                break
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                self.up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                self.down = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                self.left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                self.right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                self.space = True
            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                self.up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                self.down = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                self.right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                self.left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                self.space = False

    def update(self):
        self.listenKey()
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
                self.feather=[]
                
                self.mostrar_historia(self.level[0], 'D')
                self.construir_mapa(self.escenarios[self.escenario_index],self.player_settings)
                return;
            else:
                print("Ganasteeeeee") # mejorar aqui
                return False
        if not self.player.update(self.up, self.down, self.left, self.right, self.space, self.running, self.platforms, self.enemies, self.entities,self.gemas, self.corazon, self.feather, self.datos, self.total_level_width, self.total_level_height):
            return False
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

        self.datos.update()
        self.mostrarDatos()

    def mostrarDatos(self):
        ancho = 0

        for d in self.datos.datos:
            self.screen.blit(d, (400 + ancho,10))
            ancho =  ancho + d.get_rect()[2] + 5

    def playmusic(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1, 0.0)

    BLOCK_DATA = {
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
            "V": {"image":"feather.png", "type": Feather, "w":32, "h":32},

            "F": {"type": Player},
            " ": {"type": None}
        }

    def construir(self, x, y, player_settings, col):
        element = None
        PLATFORM_PATH = "platform/"
        ITEM_PATH = "items/"
        try:
            obj_sprite = self.BLOCK_DATA[col]
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
            elif obj_sprite["type"] == Feather:
                element = Feather(x, y, obj_sprite["w"], obj_sprite["h"], ITEM_PATH + obj_sprite["image"])
                self.feather.append(element)
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


