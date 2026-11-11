from django.urls import path
from .views import login_view, crear_usuario, pagina_inicio #, lista_bienes

urlpatterns = [
    path('',login_view, name='login'),
    path('registro/',crear_usuario,name='crear_usuario'),
    path('inicio/',pagina_inicio,name='pagina_inicio'),
    #path('bienes/', lista_bienes,name='lista_bienes'),
]