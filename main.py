# -*- coding: utf-8 -*-
import pygame, sys, os
from PIL import Image, ImageOps
import numpy
import math
from pantallas import *
from nivel import *



def main():
    global cameraX, cameraY
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()


    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), 0, 32)
    menu_items = ('Iniciar', 'Mostrar Creditos', 'Salir')
    funcs = {'Iniciar': iniciar,
             'Mostrar Creditos' : mostrar_creditos,
             'Salir': sys.exit}

    pygame.display.set_caption("Froggy!")
    timer = pygame.time.Clock()
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()
'''
    up = down = left = right = space = running = False
    #para cambiar niveles cambiar el nombre a level (no duplicados)


    player_settings = (32, 32,PATH+ "froggy.png")
    level = [# level de testeo
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
        "                                                                              S    3PPPPPPP222222222           22222222222222",
        "                                                                          3PPPPPPPP22222222222222222           22222222222222",
        "                                                                      !   22222222222222222222222222           22222222222222",
        "                                                     B               3PPPP22222222222222222222222222           22222222222222",
        "                              PP                5PPPPPP7          0PP2222222222222222222222222222222           22222222222222",
        "                                        B G      666666             66662222222222222222222222222222           22222222222222",
        "                                      PPPPPP                            6666222222222222222222222222           22222222222222",
        "        P                             622226                                662222222222222222222222           22222222222222",
        "                                       6666                                   6666666666666222222222           22222222222222",
        "                                                                               GGGGG       222222222           22222222222222",
        "    ¡  F   C                  S P  S  PB  GG  D     ¡                   D      GGGGG       222222222           22222222222222",
        "PPPPPPPPPPPPPPPPPP1          3PP2PPPPP2PPPPPPPPPPPPPPP1        P     3PPPPPPPPPPPPPPPPPPPP2222222222           22222222222222"]

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
'''
if __name__ == '__main__':
    main()
