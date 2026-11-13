import re
from django.shortcuts import render, redirect
from .models import Usuario, Ubicacion, Estado, Foto, Bien

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
            # 1. Guardamos el usuario y rol real en la sesión de Django
                request.session['nombre_usuario'] = usuario_db.nombre_usuario
                request.session['rol'] = usuario_db.rol
                return redirect('pagina_inicio')
            else:
                error = "Contraseña Incorrecta."
        except Usuario.DoesNotExist:
            error = "El usuario no esta registrado en el sistema."        

    return render(request, 'gestion/login.html',{'error': error})

#FUNCION CREAR USUARIO
""" def crear_usuario(request):
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
    
    return render(request, 'gestion/crear_usuario.html',{'error':error, 'sucess':success})      """       
#####################################USUARIO#################################
# 1. FUNCIÓN AUXILIAR (Helper para procesar el registro)
# Función interna reutilizable para validar y crear usuarios
def _procesar_creacion_usuario(request):
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
    
    return error, success    

# 2. VISTA 1: El registro público (Desde el Login, diseño centrado)
def crear_usuario_publico(request):
    error, success = _procesar_creacion_usuario(request)
    context = {'error': error, 'success': success}
    return render(request, 'gestion/crear_usuario.html', context)

# 3. VISTA 2: La gestión interna (Dentro del Dashboard, con tabla y sidebar)
def gestionar_usuario(request):
    # Reutilizamos la misma lógica de creación si envían el formulario
    error, success = _procesar_creacion_usuario(request)

    # Consultamos todos los usuarios para la tabla resumen
    usuarios = Usuario.objects.all()

    context = {
        'usuarios': usuarios,
        'error': error,
        'success': success,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario'),
        'rol_usuario': request.session.get('rol','Invitado')
    }
    return render(request,'gestion/usuario.html', context)


#FUNCION PAGINA DE INICIO
def pagina_inicio(request):
    # 2. Recuperamos los datos de la sesión (si no hay sesión, muestra valores por defecto)
    nombre_usuario = request.session.get('nombre_usuario','Usuario')
    rol_usuario = request.session.get('rol','Invitado')

    context = {
        'nombre_usuario' : nombre_usuario,
        'rol_usuario' : rol_usuario
    }
    return render(request,'gestion/pagina_inicio.html',context)

#FUNCION UBICACION
def gestionar_ubicacion(request):
    error = None
    success = None

    if request.method == 'POST':
        nombre_ubi = request.POST.get('nombre_ubicacion')
        try:
            if Ubicacion.objects.filter(nombre_ubicacion=nombre_ubi).exists():
                error = "Esta ubicacion ya se encuentra registrado."
            else:
                Ubicacion.objects.create(nombre_ubicacion=nombre_ubi)
                success = "¡Ubicacion registrada con éxito¡"
        except Exception as e:
            error = f"Error técnico: {e}"

    # Obtenemos todas las ubicaciones para mostrarlas en una tabla resumen
    ubicaciones = Ubicacion.objects.all()

    context = {
        'ubicaciones': ubicaciones,
        'error': error,
        'success': success,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario'),
        'rol_usuario': request.session.get('rol', 'Invitado') 
    }
    return render(request,'gestion/ubicacion.html', context)

#FUNCION ESTADO
def gestionar_estado(request):
    error = None
    success = None

    if request.method == 'POST':
        nombre_est = request.POST.get('nombre_estado')
        try:
            if Estado.objects.filter(nombre_estado=nombre_est).exists():
                error = "Este estado ya se encuentra registrada."
            else:
                Estado.objects.create(nombre_estado=nombre_est)
                success = "¡Estado registrado con éxito!"
        except Exception as e:
            error = f"Error técnico: {e}"
    # Obtenemos todas las ubicaciones para mostrarlas en una tabla resumen
    estados = Estado.objects.all()

    context = {
        'estados': estados,
        'error': error,
        'success': success,
        'nombre_usaurio': request.session.get('nombre_usuario', 'Usuario'),
        'rol_usuario': request.session.get('rol','Invitado')
    }
    return render(request, 'gestion/estado.html', context)

#FUNCION FOTO
def gestionar_foto(request):
    error = None
    success = None

    if request.method == 'POST':
        nombre_img = request.POST.get('nombre_foto')
        try:
            if Foto.objects.filter(nombre_foto=nombre_img).exists():
                error = "Esta Foto ya se encientra registrada."
            else:
                Foto.objects.create(nombre_foto=nombre_img)
                success = "¡Foto registrada con éxito!"
        except Exception as e:
            error = f"Error técnico: {e}"

    # Obtenemos todas las Fotos para mostrarlas en una tabla resumen
    fotos = Foto.objects.all()

    context = {
        'fotos': fotos,
        'error': error,
        'success': success,
        'nombre_usuario': request.session.get('nombre_usuario','Usuario'),
        'rol_usuario': request.session.get('rol','Invitado')
    }
    return render(request, 'gestion/foto.html', context)

def gestionar_bienes(request):
    error = None
    success = None

    if request.method == 'POST':
        # Capturamos los datos según los campos de tu modelo
        nombre = request.POST.get('nombre_bien')
        descripcion = request.POST.get('descripcion')
        placa = request.POST.get('placa')
        id_ubi = request.POST.get('ubicacion')
        id_est = request.POST.get('estado')
        id_fot = request.POST.get('foto')

        try:
            # Usamos los nombres exactos de los campos ForeignKey 
            Bien.objects.create(
                nombre_bien=nombre,
                descripcion=descripcion,
                placa=placa,
                id_ubicacion_id=id_ubi,
                id_estado_id=id_est,
                id_foto_id=id_fot
            )
            success = "¡Bien registrado con éxito!"
        except Exception as e:
            error = f"Error técnico al registra el bien: {e}"

    # Consultas para los selects y la tabla resumen
    bienes = Bien.objects.all()
    ubicaciones = Ubicacion.objects.all()
    estados = Estado.objects.all()
    fotos = Foto.objects.all()

    context = {
        'bienes': bienes,
        'ubicaciones': ubicaciones,
        'estados': estados,
        'fotos': fotos,
        'error': error,
        'success': success,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario'),
        'rol_usuario': request.session.get('rol','Invitado')
    }

    return render(request, 'gestion/bienes.html', context)                       
