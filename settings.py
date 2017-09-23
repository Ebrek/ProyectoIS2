# game options/settings
TITLE = "Froggy and the Splitters"
WIDTH = 1024
HEIGHT = 768
FPS = 60


FONT_NAME='Press Start'

#propiedades de froggy
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.6
PLAYER_JUMP = 15


#Plataformas de Inicio
#POSICION x/ POSICIOn Y, largo, altura
PLATFORM_LIST = [(-20, HEIGHT -40, WIDTH-40 , 40),
                (WIDTH + 50, HEIGHT -40, WIDTH , 40),
                (200,350,50,10),
                (150,200,40,20),
                (450,200,40,20),
                (550,200,40,20),
                (650,200,40,20),
                (20,20,80,40),
                (WIDTH-80,HEIGHT-150,180,20)]


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PERU = (205,133,63)
LIGHTBLUE = (240,248,255)
