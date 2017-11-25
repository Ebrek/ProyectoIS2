from rest_framework import serializers
from .models import Nivel, Escenario, Historia, Puntaje, AjustesGeneral

class Nivel_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Nivel
		fields = '__all__'

class Escenario_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Escenario
		fields = '__all__'

class Historia_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Historia
		fields = '__all__'

class Puntaje_Serializer(serializers.ModelSerializer):

	class Meta:
		model = Puntaje
		fields = '__all__'

class AjustesGeneral_Serializer(serializers.ModelSerializer):

	class Meta:
		model = AjustesGeneral
		fields = '__all__'
