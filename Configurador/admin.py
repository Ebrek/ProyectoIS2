from django.contrib import admin

# Register your models here.
from .models import Escenario, Nivel, AjustesGeneral, Historia
# Register your models here.

admin.site.register(Escenario)
admin.site.register(Nivel)
admin.site.register(AjustesGeneral)
admin.site.register(Historia)