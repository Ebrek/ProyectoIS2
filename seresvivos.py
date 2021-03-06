
import pygame, sys, os
from PIL import Image, ImageOps
import numpy, math
from constantes import *
from objetosestaticos import ExitBlock
from threading import Thread
from random import randint
import multiprocessing



class EnemyMosquito(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)

		self.vida=MOSQUITO_VIDA
		self.xvel_ini = MOSQUITO_xvel_ini
		self.yvel_ini = MOSQUITO_yvel_ini
		self.follow = False
		self.onGround = False
		image_path = "mosquito1.png"
		image_rect = None
		w, h = 32, 32
		try:
			image_rect = IMAGE_SIZES[PATH + image_path]
			self._image_origin = IMAGES[(PATH + image_path, w, h)]
			self._image_toLeft = IMAGES[(PATH + image_path + "-ToLeft", w, h)]
		except KeyError:
			image_rect = crop(PATH + image_path, w, h)
			IMAGE_SIZES[PATH + image_path] = image_rect
			if (PATH + image_path, w, h) not in IMAGES:
				self._image_origin = pygame.image.load(PATH + image_path)
				self._image_origin = pygame.transform.scale(self._image_origin, (w, h)).convert_alpha()
				self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
				IMAGES[(PATH + image_path, w, h)] = self._image_origin
				IMAGES[(PATH + image_path + "-ToLeft", w, h)] = self._image_toLeft
		self.rect = pygame.Rect(x, y, image_rect[0], image_rect[1])

		self.image = self._image_origin

		self.disparado = False
		self.froggy_disparo = False
	def update(self, platforms, enemies, entities, posX, posY, level_width, level_high):
		if(not self.disparado):
			self.xvel, self.yvel = self.xvel_ini, self.yvel_ini
			self.move_towards_player(posX, posY)
			self.collide(self.xvel, 0, platforms)
			self.collide(0, self.yvel, platforms)
		else:
			self.rect.x += self.xvel
			self.collide_anything(platforms, enemies, entities)
		if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width):
			self.perdervida(enemies, entities)
	def move_towards_player(self, posX, posY):
		# find normalized direction vector (dx, dy) between enemy and player
		dx, dy = self.rect.x - posX, self.rect.y - posY
		dist = math.hypot(dx, dy) #math.sqrt(dx*dx + dy*dy)
		if not self.follow:
			if dist < 400:
				self.follow = True
			else:
				return
		try:
			dx, dy = dx * -1.0 / dist, dy * -1.0 / dist
		except ZeroDivisionError:
			pass
		# move along this normalized vector towards the player at current speed
		self.xvel, self.yvel = dx * self.xvel, dy * self.yvel
		self.rect.x += self.xvel
		self.rect.y += self.yvel
		if dx > 0:
			self.image = self._image_toLeft
		else:
			self.image = self._image_origin

	def observar(self, posX, posY, platforms, enemies, entities,  level_width, level_high):
		self.update(platforms, enemies, entities, posX, posY, level_width, level_high)
		pass

	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if abs(self.rect.right - p.rect.left) < abs(self.xvel) + 1:
					self.rect.right = p.rect.left
					self.xvel = 0
					#print("Enemy collide right")
				if abs(self.rect.left - p.rect.right) < abs(self.xvel) + 1:
					self.rect.left = p.rect.right
					self.xvel = 0
					#print("Enemy collide left")
				if abs(self.rect.bottom - p.rect.top) < abs(self.yvel) + 1:
					self.rect.bottom = p.rect.top
					self.yvel = 0
				if abs(self.rect.top - p.rect.bottom) < abs(self.yvel) + 1:
					self.rect.top = p.rect.bottom
					self.yvel = 0

	def salir_disparado(self, dir):
		print("salidisparado")
		self.froggy_disparo = True
		self.disparado = True
		if dir == 'derecha':
			self.xvel = 12.0
		else:
			self.xvel = -12.0

	def salir_disparadoBoss(self, dir):
		print("salidisparado")
		self.disparado = True
		if dir == 'derecha':
			self.xvel = 6.0
		else:
			self.xvel = -6.0

	def collide_anything(self, platforms, enemies, entities):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				self.disparado = False
				self.xvel = 0
				self.perdervida(enemies, entities)
				return
		for e in enemies:
			if e != self and pygame.sprite.collide_rect(self, e):
				
				if isinstance(e, EnemySpider) or isinstance(e, EnemyMosquito):
					e.perdervida(enemies, entities)
				elif isinstance(e, EnemyBoss) and self.froggy_disparo:
					e.perdervida(enemies, entities)
					self.perdervida(enemies, entities)
				elif isinstance(e, EnemyBoss) == False:
					self.disparado = False
					self.xvel = 0
					self.perdervida(enemies, entities)
				return

	def perdervida(self, enemies, entities):
		self.vida = self.vida - 1
		if self.vida < 1: #morir
			enemies.remove(self)
			entities.remove(self)
			self = None

class EnemySpider(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		data = Conexion().obtener_ajustesgeneral()
		self.vida = SPIDER_VIDA
		self.xvel_ini = SPIDER_xvel_ini
		self.yvel_ini = SPIDER_yvel_ini
		self.follow = False
		self.onGround = False

		image_path = "spider1.png"
		image_rect = None
		w, h = 32, 32
		try:
			image_rect = IMAGE_SIZES[PATH + image_path]
			self._image_origin = IMAGES[(PATH + image_path, w, h)]
			self._image_toLeft = IMAGES[(PATH + image_path + "-ToLeft", w, h)]
		except KeyError:
			image_rect = crop(PATH + image_path, w, h)
			IMAGE_SIZES[PATH + image_path] = image_rect
			if (PATH + image_path, w, h) not in IMAGES:
				self._image_origin = pygame.image.load(PATH + image_path)
				self._image_origin = pygame.transform.scale(self._image_origin, (w, h)).convert_alpha()
				self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
				IMAGES[(PATH + image_path, w, h)] = self._image_origin
				IMAGES[(PATH + image_path + "-ToLeft", w, h)] = self._image_toLeft
		self.rect = pygame.Rect(x, y, image_rect[0], image_rect[1])

		self.image  = self._image_origin
	def update(self, platforms, enemies, entities, posX, posY, level_width, level_high):
		self.xvel, self.yvel = self.xvel_ini, self.yvel_ini
		self.move_towards_player(posX, posY)
		self.collide(self.xvel, 0, platforms)
		self.collide(0, self.yvel, platforms)
		if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width):
			self.perdervida(enemies, entities)

	def move_towards_player(self, posX, posY):
		dist = math.hypot(self.rect.x - posX, self.rect.y - posY) #math.sqrt(dx*dx + dy*dy)
		if not self.follow:
			if dist < 200:
				self.follow = True
			else:
				return
		dx = posX - self.rect.x
		self.rect.y += 4.0
		if abs(self.rect.x - posX)>3:
			if dx > 0:
				self.image = self._image_toLeft
				self.rect.x +=self.xvel
			elif dx < 0:
				self.image = self._image_origin
				self.rect.x -=self.xvel

	def observar(self, posX, posY, platforms, enemies, entities,  level_width, level_high):
		self.update(platforms, enemies, entities, posX, posY, level_width, level_high)
	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if abs(self.rect.right - p.rect.left) < abs(self.xvel)+1 and self.overlap((self.rect.top, self.rect.bottom),(p.rect.top, p.rect.bottom)):
					self.rect.right = p.rect.left
					self.xvel = 0
					#print ("Enemy collide right")
				if abs(self.rect.left - p.rect.right) < abs(self.xvel)+1 and self.overlap((self.rect.top, self.rect.bottom),(p.rect.top, p.rect.bottom)):
					self.rect.left = p.rect.right
					self.xvel = 0
					#print ("Enemy collide left")
				if abs(self.rect.bottom - p.rect.top) < abs(self.yvel)+1:
					self.rect.bottom = p.rect.top
					self.yvel = 0
				if abs(self.rect.top - p.rect.bottom) < abs(self.yvel)+1:
					self.rect.top = p.rect.bottom
					self.yvel = 0
					#print ("Enemy collide top")
	def overlap(self, t1,t2):
		return t1[0]<=t2[1] and t2[0]<=t1[0]
	def perdervida(self, enemies, entities):
		self.vida = self.vida - 1
		if self.vida < 1: #morir
			enemies.remove(self)
			entities.remove(self)
			self = None

class EnemyBoss(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		data = Conexion().obtener_ajustesgeneral()
		self.vida= 10 #data["mosquito_health"] esto debe ser cambiado por la data de la vida del boss
		self.contar = 0
		self.xvel_ini = data["mosquito_speed_x"]
		self.yvel_ini = data["mosquito_speed_y"]
		self.follow = False
		self.onGround = False
		self._image_origin = pygame.image.load(PATH + "boss_sprites/sprite_boss0.png")
		self._image_origin = pygame.transform.scale(self._image_origin, (256, 256)).convert_alpha()
		self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
		self.image  = self._image_origin
		image_rect = (self.image.get_rect().size)
		self.image.convert()
		self.rect = pygame.Rect(x, y, image_rect[0], image_rect[1])


		self.path_boss = "boss_sprites/"
		self.imagenes_izquierda = []
		self.imagenes_izquierda.append(self._image_origin)
		
		for i in range(32):# boss
			i=i+1
			im = pygame.image.load(PATH+ self.path_boss +"sprite_boss"+str(i)+".png")
			im = pygame.transform.scale(im, (256, 256)).convert_alpha()
			self.imagenes_izquierda.append(im)

		self.numero_imagen = 0
			
		self.animacion = Animacion()
		self.contar_antes_cambiar_imagen = 0
		self.numero_para_cambiar_imagen = 4

		self.enemy_get1 = None
		self.enemy_get2 = None
		

	def update(self, platforms, enemies, entities, posX, posY, level_width, level_high):
		self.xvel, self.yvel = self.xvel_ini, self.yvel_ini
##		self.move_towards_player(posX, posY)
		self.collide(self.xvel, 0, platforms)
		self.collide(0, self.yvel, platforms)
		if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width):
			self.perdervida(enemies, entities)

		self.animarBoss()
			
		self.lanzarEnemigo(enemies, entities, self.rect[0] , self.rect[1])

		print(self.vida)



	def lanzarEnemigo(self, enemies, entities, x, y):

		if self.contar == 56:
	
			lugar = 0
			cantidad = 0
			posicion =  [self.rect[3]*2/10, self.rect[3]*6/10]
			self.enemy_get1 = None
			self.enemy_get2 = None
			
			if self.numero_imagen < 5 or self.numero_imagen > 24:
				cantidad = 1
				lugar = 0
			elif self.numero_imagen > 8 and self.numero_imagen < 21:
				cantidad = 1
				lugar = 1
			else:
				cantidad = 2

			for i in range(cantidad):
			
				q = EnemyMosquito( x + self.rect[2]/4, y + posicion[lugar])
				q.follow = True
				enemies.append(q)
				entities.add(q)
				q.salir_disparadoBoss('izquierda')
				i = i + 1
				lugar = 1
				if self.enemy_get1 == None:
					self.enemy_get1 = q
				else:
					self.enemy_get2 = q
			self.contar = 0
		self.contar = self.contar + 1

	def animarBoss(self):
		
		self.contar_antes_cambiar_imagen = self.contar_antes_cambiar_imagen + 1
		
		if self.contar_antes_cambiar_imagen == self.numero_para_cambiar_imagen:
			self.contar_antes_cambiar_imagen = 0
			self.numero_imagen = self.animacion.animarIda(self.imagenes_izquierda, self.numero_imagen)
			self.image = self.imagenes_izquierda[self.numero_imagen]

	def observar(self, posX, posY, platforms, enemies, entities,  level_width, level_high):
		self.update(platforms, enemies, entities, posX, posY, level_width, level_high)
	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if abs(self.rect.right - p.rect.left) < abs(self.xvel)+1 and self.overlap((self.rect.top, self.rect.bottom),(p.rect.top, p.rect.bottom)):
					self.rect.right = p.rect.left
					self.xvel = 0
					#print ("Enemy collide right")
				if abs(self.rect.left - p.rect.right) < abs(self.xvel)+1 and self.overlap((self.rect.top, self.rect.bottom),(p.rect.top, p.rect.bottom)):
					self.rect.left = p.rect.right
					self.xvel = 0
					#print ("Enemy collide left")
				if abs(self.rect.bottom - p.rect.top) < abs(self.yvel)+1:
					self.rect.bottom = p.rect.top
					self.yvel = 0
				if abs(self.rect.top - p.rect.bottom) < abs(self.yvel)+1:
					self.rect.top = p.rect.bottom
					self.yvel = 0
					#print ("Enemy collide top")
	def overlap(self, t1,t2):
		return t1[0]<=t2[1] and t2[0]<=t1[0]
	def perdervida(self, enemies, entities):
		self.vida = self.vida - 1
		if self.vida < 1: #morir
			enemies.remove(self)
			entities.remove(self)
			self = None


class Player(Entity):
	def __init__(self, x, y, image_path):
		Entity.__init__(self)
		self.counter=0
		self.counter_lengua=0
		self.contar=0
		self.xvel = 0
		self.yvel = 0
		self.onGround = False
		self.onExitBlock = False
		self._image_origin = pygame.image.load(PATH +"sprite_froggy0.png")
		self._image_origin = pygame.transform.scale(self._image_origin, (52, 52)).convert_alpha()
		self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
		self.image  = self._image_origin
		self.jumpsound = pygame.mixer.Sound(PATH+'sounds/Froggy_Jump.wav')
		self.punchedsound = pygame.mixer.Sound(PATH+'sounds/punch.wav')
		image_rect = (32,32)#(self.image.get_rect().size)
		self.rect = pygame.Rect(x, y, image_rect[0], image_rect[1])
		self.enemy_get = None


		#todas las demas imagenes
		path_tongue = "froggy_tongue/"
		path_walk = "froggy_walk/"

		self.imagenes_derecha = []
		self.imagenes_izquierda = []

		self.imagenes_walk_derecha = []
		self.imagenes_walk_izquierda = []

		self.imagenes_derecha.append(self._image_origin)
		self.imagenes_izquierda.append(self._image_toLeft)
		for i in range(4):# lengua
			i=i+1
			im = pygame.image.load(PATH+ path_tongue+"froggy_tongue_"+str(i)+".png")
			im = pygame.transform.scale(im, (52, 52)).convert_alpha()
			self.imagenes_derecha.append(im)
			im_toLeft = pygame.transform.flip(im, True, False).convert_alpha()
			self.imagenes_izquierda.append(im_toLeft)

		self.imagenes_walk_derecha.append(self._image_origin)
		self.imagenes_walk_izquierda.append(self._image_toLeft)
		for i in range(2): #walk
			i=i+1
			im = pygame.image.load(PATH+ path_walk+"sprite_froggy"+str(i)+".png")
			im = pygame.transform.scale(im, (52, 52)).convert_alpha()
			self.imagenes_walk_derecha.append(im)
			im_toLeft = pygame.transform.flip(im, True, False).convert_alpha()
			self.imagenes_walk_izquierda.append(im_toLeft)


		self.lado = 'derecha'
		self.animacion = Animacion()
		self.agarrado = False
		self.espera = 0

		self.updates_sin_perder_vida = 30
		self.contador_sin_perder_vida = 30

		self.forma = [0, 'ida']

		self.forma_walk = [0, 'ida']
		self.sacandolengua=False
	def update(self, up, down, left, right, space, running, platforms, enemies, entities, gemas,corazon,feather, datos, level_width, level_high):
		vida = True
		global gravedad

		if up:
			# only jump if on the ground
			if self.onGround:
				self.yvel -= gravedad
				try:
					self.jumpsound.stop()
					self.jumpsound.play()

				except Exception:
					print("no audio")
		if down:
			pass
		#if running:
			#self.xvel = 12
		if not self.sacandolengua:
			if left:
				self.xvel = -6.3
				self.lado = 'izquierda'
			if right:
				self.xvel = 6.3
				self.lado = 'derecha'

		#franco
		if self.agarrado == True:
								# Con esto se espera un tiempo hasta poder lanzar el mosquito
			self.espera = self.espera + 1
			#print(self.espera)

			if self.espera >= 15:

					####### ahora puse que tenga que tenerlo
				if space== True:
					#print('xxxxxxxxxxxxxxxxxx')
					enemies.append(self.enemy_get)
					entities.add(self.enemy_get)
					self.enemy_get.rect.x=self.rect.x
					self.enemy_get.rect.y=self.rect.y
					self.enemy_get.salir_disparado(self.lado)
					self.espera = 0
					self.agarrado = False

		if self.espera < 15 and self.agarrado == False:
			self.espera = self.espera + 1

		if space and self.sacandolengua==False:
			self.sacandolengua = True
		if self.sacandolengua == True:
			#cambiar imagen
			self.sacarlengua(self.lado)
			if abs(self.xvel) > 0.2:
				self.xvel =  self.xvel - numpy.sign(self.xvel)*0.1
			else:
				self.xvel = 0

		if not self.onGround:
			# only accelerate with gravity if in the air
			self.yvel += 0.3
			# max falling speed
			if self.yvel > 100:
				self.yvel = 100
		if not(left or right):
			self.xvel = 0
			self.forma_walk = [0, 'ida']
			if self.sacandolengua == False:
				if self.lado == 'izquierda':
					self.image = self.imagenes_walk_izquierda[self.forma_walk[0]]
				else:
					self.image = self.imagenes_walk_derecha[self.forma_walk[0]]
		elif self.sacandolengua == False:
			self.walkloop(self.lado)
			if self.lado == 'izquierda':
				self.image = self.imagenes_walk_izquierda[self.forma_walk[0]]
			else:
				self.image = self.imagenes_walk_derecha[self.forma_walk[0]]
		# increment in x direction
		self.rect.left += self.xvel
		# do x-axis collisions
		self.collide(self.xvel, 0, platforms)
		# increment in y direction
		self.rect.top += self.yvel
		# assuming we're in the air
		self.onGround = False;
		# do y-axis collisions
		self.collide(0, self.yvel, platforms)
		vida = self.collide_enemies(enemies, entities, datos)
		self.beobserver(enemies, platforms, entities,  level_width, level_high)
		self.collide_gemas(gemas, entities, datos)
		self.collide_corazon(corazon,entities,datos)
		self.collide_feather(feather,entities,datos)
		if(self.rect.y > level_high or self.rect.right < 0 or self.rect.left > level_width or vida == False):
			return False
		else:
			return True



	def sacarlengua(self, dir):
		self.counter_lengua = self.counter_lengua + 1
		if self.counter_lengua > 40:
			self.counter_lengua = 0
			self.sacandolengua = False
			self.forma = [0, 'ida']
		elif self.counter_lengua % 5 == 0:
			#print(self.counter_lengua)
			if dir == 'derecha':
				self.forma = self.animacion.animarCompleta(self.imagenes_derecha, self.forma)
				self.image = self.imagenes_derecha[self.forma[0]]
			else:
				self.forma = self.animacion.animarCompleta(self.imagenes_izquierda, self.forma)
				self.image = self.imagenes_izquierda[self.forma[0]]

	def walkloop(self, dir):
		self.counter = self.counter + 1
		if self.counter > 50:
			self.counter = 0
		elif self.counter % 10 == 0:
			#print(self.counter)
			if dir == 'derecha':
				self.forma_walk = self.animacion.animarCompleta(self.imagenes_walk_derecha, self.forma_walk)
				self.image = self.imagenes_walk_derecha[self.forma_walk[0]]
			else:
				self.forma_walk = self.animacion.animarCompleta(self.imagenes_walk_izquierda, self.forma_walk)
				self.image = self.imagenes_walk_izquierda[self.forma_walk[0]]

	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if isinstance(p, ExitBlock):
					#se va al siguiente nivel
					self.onExitBlock = True
				if xvel > 0:
					self.rect.right = p.rect.left
					#print("collide right")
				if xvel < 0:
					self.rect.left = p.rect.right
					#print("collide left")
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.yvel = 0
				if yvel < 0:
					self.rect.top = p.rect.bottom
					self.yvel = 0

	def collide_enemies(self, enemies, entities, datos):
		global gravedad
		sigue_vivo = True
		for e in enemies:
			if isinstance(e, EnemyMosquito) and self.agarrado == False and self.forma[0] != 0 and self.espera == 15:
				self.agarrado = self.agarrarObjeto(e)


				if self.agarrado == True:
					# Se remueve el mosquito para que paresca que es comido y se agrega a enemy_get
					self.enemy_get = e

					enemies.remove(e)
					entities.remove(e)
					self.espera = 0

			# este es para que el enemigo tragado no le haga perder vida
			if e == self.enemy_get:
				pass


			# aca es para todos los demas enemigos
			elif pygame.sprite.collide_rect(self, e) :
				if self.contador_sin_perder_vida == self.updates_sin_perder_vida:
					self.perder_vida(datos)
					if datos.vidas_restantes == 0:
						sigue_vivo = False
						gravedad ==9.3
					self.contador_sin_perder_vida = 0
					return sigue_vivo
				else:
					self.contador_sin_perder_vida = self.contador_sin_perder_vida + 1
		return sigue_vivo


	def perder_vida(self, datos):
		global gravedad
		try:
			self.punchedsound.play()
		except Exception:
			print("no audio")
		datos.vidas_restantes = datos.vidas_restantes - 1
		print("vida" + str(datos.vidas_restantes))
		print(gravedad)
		if (gravedad==9.3):
			pass
		elif gravedad != 9.3:
			gravedad = gravedad-3
			print("perdiste feather")



	def ganar_vida(self, datos):
		datos.vidas_restantes = datos.vidas_restantes + 1
		print("vida" + str(datos.vidas_restantes))


	def collide_gemas(self, gemas, entities, datos):
		for e in gemas:
			cogio_gema = False

			cogio_gema = self.agarrarObjeto(e)

			if(cogio_gema == True):
				datos.puntaje = datos.puntaje + e.valor
				entities.remove(e)
				gemas.remove(e)

		return False

	def collide_corazon(self, corazon, entities, datos):
		for e in corazon:
			cogio_corazon = False

			cogio_corazon= self.agarrarObjeto(e)

			if(cogio_corazon == True):
				datos.vidas_restantes = datos.vidas_restantes + 1
			#	ganar_vida()
				entities.remove(e)
				corazon.remove(e)

		return False

	def collide_feather(self, feather, entities, datos):
		global gravedad
		for e in feather:
			cogio_feather = False
			cogio_feather= self.agarrarObjeto(e)
			if(cogio_feather == True):
				if (gravedad==9.3):
					gravedad = gravedad + 3
				elif gravedad != 9.3:
					pass

				entities.remove(e)
				feather.remove(e)

		return False


	def perder_salto(self,entities,datos):
		global gravedad
		if (gravedad==9.3):
			gravedad = gravedad + 3
		elif gravedad != 9.3:
			pass

	def beobserver(self, enemies, platforms, entities, level_width, level_high):
		for q in enemies:
			if isinstance(q, EnemyMosquito):
				q.observar(self.rect.x, self.rect.y, platforms, enemies, entities, level_width, level_high)
			else:
				q.observar(self.rect.x, self.rect.y, platforms, enemies, entities, level_width, level_high)

	def agarrarObjeto(self, objeto):
		agarro = False
		return pygame.sprite.collide_rect(self, objeto)

class Animacion:
	def __init__(self):
		pass

	def animarCompleta(self, imagenes, forma):
		# es +1 ya que en la ultima posicion va a ir si es ida o vuelta
		if forma[0] + 1 == len(imagenes):
			forma[1] = 'vuelta'
		# se verifica si esta en la ida o vuelta
		if forma[1] == 'ida':
			forma[0] = forma[0] + 1
		elif forma[1] == 'vuelta':
			forma[0] = forma[0] - 1
			if forma[0] == 0:
				forma[1] = 'ida'
		return forma

	def animarIda(self, imagenes, i):

		# es +1 ya que aca no hay ida o vuelta
		if i + 1 == len(imagenes):
			i = 0
		else:
			i = i + 1
		return i


if __name__ == "__main__":
	main()
