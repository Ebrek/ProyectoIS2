import pygame
import sys
import Resources.pygame_textinput
from constantes import *
pygame.init()


class Pantalla_Puntuacion():

    def __init__(self ):
        #self.bg=bg
        # Create TextInput-object
        self.textinput = Resources.pygame_textinput.TextInput(text_color=OLIVE)
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_text(self,text,size,color,x,y):
        font = pygame.font.Font("freesansbold.ttf", size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def mostrar(self):
        while True:
            self.screen.fill((0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        #some codes
                        print(self.textinput.get_text())

            # Feed it with events every frame
            if len(self.textinput.get_text()) < 25 and pygame.K_DELETE in events:
                self.textinput.update(events)
            # Blit its surface onto the screen
            self.screen.blit(self.textinput.get_surface(), (180, WIN_HEIGHT-45))


            self.draw_text("Jugador:",32,WHITE,100,WIN_HEIGHT-50)
            pygame.display.update()
            self.clock.tick(30)

b = Pantalla_Puntuacion()
b.mostrar()