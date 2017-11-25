# -*- coding: utf-8 -*-
import pygame
from pantallas import Pantalla_Inicio
from constantes import DISPLAY, FLAGS, DEPTH



def main():
    global cameraX, cameraY
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)

    pantalla_inicio = Pantalla_Inicio(screen)
    pantalla_inicio.run()

if __name__ == '__main__':
    main()
