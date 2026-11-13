from django.urls import path
from .views import login_view, crear_usuario_publico, pagina_inicio, gestionar_ubicacion, gestionar_estado, gestionar_foto, gestionar_usuario, gestionar_bienes #, lista_bienes

urlpatterns = [
    path('',login_view, name='login'),
    path('registro/',crear_usuario_publico,name='crear_usuario_publico'),
    path('inicio/',pagina_inicio,name='pagina_inicio'),
    path('ubicacion/', gestionar_ubicacion, name='gestionar_ubicacion'),
    path('estado/', gestionar_estado, name='gestionar_estado'),
    path('foto/', gestionar_foto, name='gestionar_foto'),
    path('usuario', gestionar_usuario, name='gestionar_usuario'),
    path('bienes/', gestionar_bienes,name='gestionar_bienes'),
]