import pygame
import sys
import Resources.pygame_textinput
from constantes import *
from conexion import Conexion
pygame.init()


class Pantalla_Puntuacion():

    def __init__(self, nivel_id, puntaje):
        #self.bg=bg
        # Create TextInput-object
        self.textinput = Resources.pygame_textinput.TextInput(text_color=OLIVE)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.data = Conexion().obtener_puntaje(nivel_id)
        self.data_nivel= Conexion().obtener_nivel(nivel_id)
        self.puntaje = puntaje

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
        while True:
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
                        print(self.textinput.get_text())
                        # TODO retorna la wea
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

b = Pantalla_Puntuacion(2,None)
b.mostrar()