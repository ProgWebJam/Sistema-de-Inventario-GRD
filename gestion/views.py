import re
from django.shortcuts import render, redirect
from .models import Usuario #, lista_bienes # Asegúrate de tener tu modelo Usuario importado

# FUNCIO DE LOGEO.
def login_view(request):
    #Declarar variale
    error = None
    #Condicion si el metodo de envio de datos es iguala POST
    if request.method == 'POST':
        #Declara las variables e igualarlas a lo que trae en la base de datos
        nombre_ingreso = request.POST.get('nombre_usuario')
        password_ingreso = request.POST.get('password')

        try:
            usuario_db = Usuario.objects.get(nombre_usuario=nombre_ingreso)
            if usuario_db.password == password_ingreso:
                return redirect('pagina_inicio')
            else:
                error = "Contraseña Incorrecta."
        except Usuario.DoesNotExist:
            error = "El usuario no esta registrado en el sistema."        

    return render(request, 'gestion/login.html',{'error': error})

#FUNCION CREAR USUARIO
def crear_usuario(request):
    error = None
    success = None
    if request.method == 'POST':
        nombre = request.POST.get('nombre_usuario')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        #-----VALIDAR SEGURIDAD CONTRASEÑA-----#
        #Validar que la contraseña sea igual o mayor a 8 caracteres
        if len(password) < 8:
            error = "La contraseña debe tener al menos 8 caracteres."
        #Validar que la contraseña tenga al menos una mayuscula
        elif not re.search(r'[A-Z]',password):
            error = "La contraseña debe contener al menos una letra mayúscula."
        #Validar que la contraseña tenga al menos una minuscula
        elif not re.search(r'[a-z]',password):
            error = "La contraseña debe contener al menos una letra minúscula."
        #Validar que la contraseña tenga caracter especial    
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+]',password):
            error = "La contraseña debe contener al menos un carácter especial (ej. @, #, $, etc.)."
        else:
            try:
                #Validar que no alla usuario duplicado
                if Usuario.objects.filter(nombre_usuario=nombre).exists():
                    error = "El nombre de usuario ya se encuentra resgistrado."
                else:
                    Usuario.objects.create(
                        nombre_usuario=nombre,
                        password=password,
                        rol=rol
                    )
                    success = "¡Usuario creado con Exito! Ya puede iniciar sesion."
            except Exception as e:
                #error = "Error: El nombre de usuario ya existe o los datos son invalido. "
                error = f"Error técnico de BD: {e}" 
    
    return render(request, 'gestion/crear_usuario.html',{'error':error, 'sucess':success})            

#FUNCION PAGINA DE INICIO
def pagina_inicio(request):
    return render(request,'gestion/pagina_inicio.html')