
import pygame, sys, os
from constantes import *



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

        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
            self.image = IMAGES[(PATH + image_path, w, h)]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path, w, h) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (w, h)).convert_alpha()
                IMAGES[(PATH + image_path, w, h)] = self.image
        self.rect = pygame.Rect(x, y - h + 32, image_rect[0], image_rect[1])

    def update(self):
        pass

#############################################################################################
class Gemas(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
            self.image = IMAGES[(PATH + image_path, w, h)]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path, w, h) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (w, h)).convert_alpha()
                IMAGES[(PATH + image_path, w, h)] = self.image
        self.rect = pygame.Rect(x, y - h + 32, image_rect[0], image_rect[1])

        self.valor = 20

    def update(self):
        pass
################################################################################################


class Corazon(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
            self.image = IMAGES[(PATH + image_path, w, h)]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path, w, h) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (w, h)).convert_alpha()
                IMAGES[(PATH + image_path, w, h)] = self.image
        self.rect = pygame.Rect(x, y - h + 32, image_rect[0], image_rect[1])

        self.valor = 20

    def update(self):
        pass

###############################################################################################
class Feather(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)
        image_rect = None
        try:
            image_rect = IMAGE_SIZES[PATH + image_path]
            self.image = IMAGES[(PATH + image_path, w, h)]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path, w, h) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (w, h)).convert_alpha()
                IMAGES[(PATH + image_path, w, h)] = self.image
        self.rect = pygame.Rect(x, y - h + 32, image_rect[0], image_rect[1])

        self.valor = 20

    def update(self):
        pass

#############################################################################################

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y, "platform/18.png")
