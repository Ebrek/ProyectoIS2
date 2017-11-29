"""ProyectoIS2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from Configurador import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^niveles/$', views.Nivel_Lista.as_view()),
    url(r'^niveles/(?P<pk>[0-9]+)/', views.Nivel_Detalle.as_view()),

    url(r'^escenarios/$', views.Escenario_Lista.as_view()),
    url(r'^escenarios/(?P<pk>[0-9]+)/', views.Escenario_Detalle.as_view()),

    url(r'^historias/(?P<pk>.+)/$', views.Historia_Lista.as_view()),
    url(r'^historias/(?P<pk>[0-9]+)/', views.Historia_Detalle.as_view()),
    url(r'^historias/$', views.Historia_Lista.as_view()),
    
    url(r'^puntajes/$', views.Puntaje_Lista.as_view()),
    url(r'^puntajes/(?P<pk>[0-9]+)/', views.Puntaje_Detalle.as_view()),

    url(r'^ajustesgenerales/$', views.AjustesGeneral_Lista.as_view()),
    url(r'^ajustesgenerales/(?P<pk>[0-9]+)/', views.AjustesGeneral_Detalle.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
'''
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
