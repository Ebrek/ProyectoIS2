import pygame
from PIL import Image, ImageOps
import numpy, math


WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

WHITE = (255, 255, 255)
OLIVE = (107, 142, 35)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

gravedad= 9.3


from conexion import Conexion
AJUSTES_GENERALES = Conexion().obtener_ajustesgeneral()
MOSQUITO_VIDA = AJUSTES_GENERALES["mosquito_health"]
MOSQUITO_xvel_ini = AJUSTES_GENERALES["mosquito_speed_x"]
MOSQUITO_yvel_ini = AJUSTES_GENERALES["mosquito_speed_y"]

SPIDER_VIDA = AJUSTES_GENERALES["spider_health"]
SPIDER_xvel_ini = AJUSTES_GENERALES["spider_speed_x"]
SPIDER_yvel_ini = AJUSTES_GENERALES["spider_speed_y"]

FROGGY_VIDA = AJUSTES_GENERALES["froggy_health"]

FPS_RATE = 60
IMAGE_SIZES = {}
IMAGES = {}
PATH = "Resources/"

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def simple_camera(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

    def complex_camera(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return pygame.Rect(l, t, w, h)

def crop(image_name, rx, ry):
        pil_image = Image.open(image_name)
        size = (pil_image.width, pil_image.height)
        np_array = numpy.array(pil_image)
        blank_px = [255, 255, 255, 0]
        mask = np_array != blank_px
        coords = numpy.argwhere(mask)
        try:
            x0, y0, z0 = coords.min(axis=0)
            x1, y1, z1 = coords.max(axis=0) + 1
            cropped_box = np_array[x0:x1, y0:y1, z0:z1]
            pil_image = Image.fromarray(cropped_box, 'RGBA')
        except Exception:
            pass
        print(image_name + str((pil_image.width, pil_image.height)))
        return (pil_image.width * rx / size[0], pil_image.height * ry / size[1])
