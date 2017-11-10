from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.


class Nivel(models.Model):

	#contiene path de audio y path de imagen de fondo
	title = models.CharField(max_length=50)
	bg_music = models.FileField(upload_to='bg_music/')
	bg_image = models.FileField(upload_to='bg_images/')

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

class Escenario(models.Model):

	#contiene archivos de niveles
	title = models.CharField(max_length=50)
	mapa = models.FileField(upload_to='maps/')
	nivel  = models.ForeignKey(Nivel, on_delete=models.CASCADE)
	order = models.PositiveIntegerField(validators=[MinValueValidator(1)])

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

class AjustesGeneral(models.Model):

	#contine parametros generales
	title = models.CharField(max_length=50)
	froggy_health = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	spider_health = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	spider_speed_x = models.FloatField(validators=[MinValueValidator(0)])
	spider_speed_y = models.FloatField(validators=[MinValueValidator(0)])
	mosquito_health = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	mosquito_speed_x = models.FloatField(validators=[MinValueValidator(0)])
	mosquito_speed_y = models.FloatField(validators=[MinValueValidator(0)])

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title
