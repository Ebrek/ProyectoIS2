
import pygame, sys, os
from PIL import Image, ImageOps
import numpy, math
from constantes import *

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


class Platform(Entity):
    def __init__(self, x, y, image_path):
        Entity.__init__(self)

        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
            self.image = IMAGES[(PATH + image_path, 32, 32)]
        except KeyError:
            image_rect = crop(PATH + image_path, 32, 32)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path, 32, 32) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (32, 32)).convert_alpha()
                IMAGES[(PATH + image_path, 32, 32)] = self.image
        self.rect = pygame.Rect(x, y, image_rect[0], image_rect[1])

    def update(self):
        pass


class Decoration(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        self._image_origin = pygame.image.load(PATH + image_path)
        self._image_origin = pygame.transform.scale(self._image_origin, (w, h))
        self.image = self._image_origin
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
        self.rect = pygame.Rect(x, y - h + 32, image_rect[0], image_rect[1])

    def update(self):
        pass

#############################################################################################
class Gemas(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        self._image_origin = pygame.image.load(PATH + image_path)
        self._image_origin = pygame.transform.scale(self._image_origin, (w, h))
        self.image = self._image_origin
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
        self.rect = pygame.Rect(x, y - h + 32, image_rect[0], image_rect[1])

        self.valor = 20

    def update(self):
        pass
#############################################################################################

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y, "platform/18.png")

