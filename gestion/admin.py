from django.contrib import admin
from .models import Bien, Ubicacion, Usuario, Estado, Foto

admin.site.register(Bien)
admin.site.register(Ubicacion)
admin.site.register(Usuario)
admin.site.register(Estado)
admin.site.register(Foto)
