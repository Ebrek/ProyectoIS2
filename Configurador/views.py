from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import render
from django.http import Http404
from rest_framework import generics
from django.http import JsonResponse
from django.http import HttpResponse
from django.core import serializers
from rest_framework.parsers import JSONParser
# Create your views here.

class Nivel_Lista(generics.ListCreateAPIView):
	model = Nivel
	serializer_class = Nivel_Serializer
	def get_queryset(self):
		queryset = Nivel.objects.all()
		nivel_id = self.request.query_params.get('nivel_id', None)

		if nivel_id is not None:
			queryset = queryset.filter(nivel_id=nivel_id)
		#serializer = Nivel_Serializer(queryset, many=True)

		#data = serializers.serialize('json', queryset)
		#return HttpResponse(serializer.data, content_type="application/json")
		return queryset
	#def get(self, request):
	#	niveles = Nivel.objects.all()
	#	serializer = Nivel_Serializer(niveles, many=True)
	#	return Response(serializer.data)

	def post(self, request):
		serializer = Nivel_Serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Nivel_Detalle(APIView):
	def get_object(self, pk):
		try:
			return Nivel.objects.get(pk=pk)
		except Stock.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Nivel_Serializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Nivel_Serializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class Escenario_Lista(generics.ListCreateAPIView):
	model = Escenario
	serializer_class = Escenario_Serializer

	# Show all of the PASSENGERS in particular WORKSPACE
	# or all of the PASSENGERS in particular AFIRLINE
	def get_queryset(self):
		queryset = Escenario.objects.all()
		nivel_id = self.request.query_params.get('nivel_id', None)

		if nivel_id is not None:
			queryset = queryset.filter(nivel_id=nivel_id)
		return queryset

	#def get(self, request):
	#	escenarios = Escenario.objects.all()
	#	serializer = Escenario_Serializer(escenarios, many=True)
	#	return Response(serializer.data)

	def post(self, request):
		serializer = Escenario_Serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Escenario_Detalle(APIView):
	def get_object(self, pk):
		try:
			return Escenario.objects.get(pk=pk)
		except Stock.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Escenario_Serializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Escenario_Serializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class Historia_Lista(generics.ListCreateAPIView):
	model = Historia
	serializer_class = Historia_Serializer

	# Show all of the PASSENGERS in particular WORKSPACE
	# or all of the PASSENGERS in particular AFIRLINE
	def get_queryset(self):
		queryset = Historia.objects.all()
		suceso = self.request.query_params.get('suceso', None)
		escenario_id = self.request.query_params.get('escenario_id', None)

		if suceso is not None:
			queryset = queryset.filter(suceso=suceso)
		if escenario_id is not None:
			queryset = queryset.filter(escenario_id=escenario_id)

		return queryset

	#def get(self, request):
	#	historias = Historia.objects.all()
	#	serializer = Historia_Serializer(historias, many=True)
	#	return Response(serializer.data)

	def post(self, request):
		serializer = Historia_Serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Historia_Detalle(APIView):
	def get_object(self, pk):
		try:
			return Historia.objects.get(pk=pk)
		except Stock.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Historia_Serializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Historia_Serializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class Puntaje_Lista(generics.ListCreateAPIView):
	model = Puntaje
	serializer_class = Puntaje_Serializer

	# Show all of the PASSENGERS in particular WORKSPACE
	# or all of the PASSENGERS in particular AFIRLINE
	def get_queryset(self):
		queryset = Puntaje.objects.all()
		nivel_id = self.request.query_params.get('nivel_id', None)

		if nivel_id is not None:
			queryset = queryset.filter(nivel_id=nivel_id)
		return queryset

	#def get(self, request):
	#	puntajes = Puntaje.objects.all()
	#	serializer = Puntaje_Serializer(puntajes, many=True)
	#	return Response(serializer.data)
	@csrf_exempt
	def post(self, request):
		print(request.POST)
		#data = JSONParser().parse(request)
		serializer = Puntaje_Serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class Puntaje_Detalle(APIView):
	def get_object(self, pk):
		try:
			return Puntaje.objects.get(pk=pk)
		except Stock.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Puntaje_Serializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk):
		snippet = self.get_object(pk)
		serializer = Puntaje_Serializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class AjustesGeneral_Lista(APIView):

	def get(self, request):
		ajuestesGenerales = AjustesGeneral.objects.all()
		serializer = AjustesGeneral_Serializer(ajuestesGenerales, many=True)
		return Response(serializer.data)

	def post(self, request):
		data = JSONParser().parse(request)
		serializer = AjustesGeneral_Serializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
		return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AjustesGeneral_Detalle(APIView):
	def get_object(self, pk):
		try:
			return AjustesGeneral.objects.get(pk=pk)
		except Stock.DoesNotExist:
			raise Http404

	def get(self, request, pk):
		snippet = self.get_object(pk)
		serializer = AjustesGeneral_Serializer(snippet)
		return Response(serializer.data)

	def put(self, request, pk):
		snippet = self.get_object(pk)
		serializer = AjustesGeneral_Serializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
		
