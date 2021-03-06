
import pygame, sys
from constantes import *
import Resources.pygame_textinput

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

            self.clock.tick(FPS_RATE)

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
            image = pygame.transform.scale(image,(450,200)).convert_alpha()
            image_width, image_height= image.get_size()
            self.screen.blit(image,((WIN_WIDTH-image_width)/2,(WIN_HEIGHT-image_height)/6))


            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mposx, mposy)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()

class Pantalla_Inicio():
    def __init__(self, screen):
        self.screen = screen
        funcs = {'Seleccionar nivel': self.iniciar,
                 'Mostrar puntuación': self.mostrar_highscore,
                 'Mostrar Créditos' : self.mostrar_creditos,
                 'Salir del juego': sys.exit}
        pygame.display.set_caption("Froggy!")
        self.gameMenu = GameMenu(screen, funcs.keys(), funcs)

    def run(self):
        self.gameMenu.run()

    def iniciar(self, param):
        from nivel import Partida
        partida = Partida(param.screen)
        partida.mostrar_pantalla_niveles()

    def mostrar_highscore(self, param):
        hig = HighScore(param.screen)
        hig.mostrar_pantalla_highsoce()

    def mostrar_creditos(self, screen):
        screen = pygame.display.set_mode((800, 600))
        screen_r = screen.get_rect()
        font = pygame.font.SysFont("freesansbold.ttf", 40)
        clock = pygame.time.Clock()
        credit_list = ["CREDITOS", " ",  "Froggy and the Spitters", " ", "DESARROLLADORES", " ", "Leo Wong Law", " ", "Angel Wong Law", " ", "Joan Pinto Albornoz", " ", "Franco Casanova Gonzalez", " ", "Aaron Aguero Estrella"]
        texts =[]
        for i, line in enumerate(credit_list):
            s = font.render(line,1,OLIVE)
            r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
            texts.append((r, s))
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return

            screen.fill((0, 0, 0))

            for r, s in texts:

                r.move_ip(0, -1)

                screen.blit(s, r)


            if not screen_r.collidelistall([r for (r, _) in texts]):
                return


            pygame.display.flip()

        
            clock.tick(60)


class Datos_partida():
    def __init__(self, image_path_gema, image_path_vida, image_path_feather, letra_datos, vidas_inicio):
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

        #imagen Feather
        #self._image_feather = pygame.image.load(PATH + image_path_gema)
        #self._image_feather = pygame.transform.scale(self._image_feather, (self.datos[0].get_rect()[3], self.datos[0].get_rect()[3])).convert_alpha()
        #self.datos.append( self._image_feather )


        #self.screen.blit(imagenTextoPresent, (400, 10))
        #self.screen.blit(imagenTextoPresent, (400 + imagenTextoPresent.get_rect()[2], 10))


    def update(self):
        self.datos[0] = self.letra.render(str(self.puntaje), True, (100,200,0), None )
        self.datos[2] = self.letra.render(str(self.vidas_restantes), True, (100,200,0), None )



class Pantalla_Puntuacion():

    def __init__(self, nivel_id, puntaje, screen):
        #self.bg=bg
        # Create TextInput-object
        self.textinput = Resources.pygame_textinput.TextInput(text_color=OLIVE)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.data = Conexion().obtener_puntaje(nivel_id)
        self.data_nivel= Conexion().obtener_nivel(nivel_id)
        self.puntaje = puntaje
        self.nivel_id = nivel_id
    def draw_text(self,text,size,color,x,y, midtop=True):
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        if midtop:
            text_rect.midtop = (x,y)
        else:
            text_rect.midleft = (x,y)
        self.screen.blit(text_surface, text_rect)

    def mostrar(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            backspace = False
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        #some codes
                        if self.puntaje != None:
                            print(self.textinput.get_text())
                            r = requests.post(URL + 'puntajes/', data={'player': self.textinput.get_text(), 'puntaje': self.puntaje, 'nivel': self.nivel_id})
                            print(r.status_code, r.reason)
                        # TODO retorna la wea
                        running = False
                    if event.key==pygame.K_BACKSPACE:
                        backspace = True
                if event.type==pygame.KEYUP and event.key==pygame.K_BACKSPACE:
                    backspace = False
            pos_w_ini = 100
            pos_y_ini = 200
            count_y_ini = 0
            count_pos = 1
            for element in self.data:
                self.draw_text(str(count_pos) + ")  " + element["player"], 32, LIGHT_YELOW, pos_w_ini, pos_y_ini + count_y_ini, midtop=False)
                self.draw_text(str(element["puntaje"]), 32, LIGHT_BLUE, pos_w_ini + 400, pos_y_ini + count_y_ini, midtop=False)
                count_y_ini += 30
                count_pos += 1
            self.draw_text(self.data_nivel["title"], 32, RED, WIN_WIDTH/2, 50)

            if self.puntaje != None:
                self.draw_text("Jugador:", 32, WHITE, 50, WIN_HEIGHT - 50, midtop=False)
                self.draw_text("Jugador:", 32, WHITE, 50, WIN_HEIGHT - 50, midtop=False)
                # Feed it with events every frame
                if len(self.textinput.get_text()) < 15 or backspace:
                    self.textinput.update(events)
                elif len(self.textinput.get_text()) >= 14:
                    pygame.event.clear()
                # Blit its surface onto the screen
                self.screen.blit(self.textinput.get_surface(), (200, WIN_HEIGHT-60))
                self.draw_text(str(self.puntaje), 32, RED, WIN_WIDTH-200, WIN_HEIGHT - 50, midtop=False)


            pygame.display.update()
            self.clock.tick(60)

class HighScore():
    def __init__(self, screen):
        #para cambiar niveles cambiar el nombre a level (no duplicados)
        self.screen = screen

        self.niveles_data = Conexion().listar_niveles()

    def mostrar_pantalla_highsoce(self):

        screen = self.screen
        niveles_funciones = {}
        def function_builder(nivel_id, puntaje, screen):
            def function(param):
                param.mainloop=False
                p = Pantalla_Puntuacion(nivel_id, puntaje, screen)
                p.mostrar()
            return function
        for element in self.niveles_data:
            niveles_funciones[element["title"]] = function_builder(element["id"], None, screen)

        def mini_function(param):
            param.mainloop=False
        niveles_funciones["Pantalla principal"] = mini_function

        pygame.display.set_caption("Froggy!")
        timer = pygame.time.Clock()
        gm = GameMenu(screen, niveles_funciones.keys(), niveles_funciones)
        gm.run()




'''
class Media_Screen():
    def __init__(self, timer, bg):
        self.timer = timer
        #self.bg=bg
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.timer.tick(FPS_RATE)
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

class Start_Screen(Media_Screen):
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
