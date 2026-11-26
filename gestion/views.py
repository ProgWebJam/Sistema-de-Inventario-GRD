import re
from django.shortcuts import render, redirect, get_object_or_404
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
def _validar_password_usuario(password):

        #-----VALIDAR SEGURIDAD CONTRASEÑA-----#
        #Validar que la contraseña sea igual o mayor a 8 caracteres
        if len(password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."
        #Validar que la contraseña tenga al menos una mayuscula
        elif not re.search(r'[A-Z]',password):
            return "La contraseña debe contener al menos una letra mayúscula."
        #Validar que la contraseña tenga al menos una minuscula
        elif not re.search(r'[a-z]',password):
            return "La contraseña debe contener al menos una letra minúscula."
        #Validar que la contraseña tenga caracter especial    
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+]',password):
            return "La contraseña debe contener al menos un carácter especial (ej. @, #, $, etc.)."
               
        return None  

# 2. VISTA 1: El registro público (Desde el Login, diseño centrado)
""" def crear_usuario_publico(request):
    error, success = _procesar_creacion_usuario(request)
    context = {'error': error, 'success': success}
    return render(request, 'gestion/crear_usuario.html', context) """

# 3. VISTA 2: La gestión interna (Dentro del Dashboard, con tabla y sidebar)
def gestionar_usuario(request):
    # Reutilizamos la misma lógica de creación si envían el formulario
    #error, success = _procesar_creacion_usuario(request)

    error = None
    success = None
    usuario_editar = None

    editar_id = request.GET.get('editar')

    if editar_id:
        usuario_editar = get_object_or_404(Usuario, pk=editar_id)

    if request.method == 'POST':
        nombre = (request.POST.get('nombre_usuario') or '').strip()
        password = request.POST.get('password') or ''
        rol = request.POST.get('rol')
        id_registro = request.POST.get('id_usuario')

        try:
            #MODO EDITAR
            if id_registro:
                usuario_obj = get_object_or_404(Usuario, pk=id_registro)

                if Usuario.objects.filter(nombre_usuario=nombre).exclude(pk=usuario_obj.pk).exists():
                    error = "El nombre de usuario ya se encuentra registrado."
                elif password:
                    error_pwd = _validar_password_usuario(password)
                    if error_pwd:
                        error = error_pwd
                    else:
                        usuario_obj.nombre_usuario = nombre
                        usuario_obj.rol = rol
                        usuario_obj.password = password
                        usuario_obj.save()
                        success = "¡Usuario actualizado con éxito!"
                        usuario_editar = None
                else:
                    # Si no se escribe nueva contraseña al editar, se mantiene la actual
                    usuario_obj.nombre_usuario = nombre
                    usuario_obj.rol = rol
                    usuario_obj.save()
                    success = "¡Usuario actualizado con éxito!"
                    usuario_editar = None
            
            #MODO CREAR
            else:
                if Usuario.objects.filter(nombre_usuario=nombre).exists():
                    error = "El nombre de usuario ya se encuentra registrado."
                else:
                    error_pwd = _validar_password_usuario(password)
                    if error_pwd:
                        error = error_pwd
                    else:
                        Usuario.objects.create(
                            nombre_usuario=nombre,
                            password=password,
                            rol=rol
                        )
                        success = "¡Usuario creado con éxito!"

        except Exception as e:
            #error = "Error: El nombre de usuario ya existe o los datos son invalido. "
            error = f"Error técnico de BD: {e}" 

    # Consultamos todos los usuarios para la tabla resumen
    usuarios = Usuario.objects.all()

    context = {
        'usuarios': usuarios,
        'usuario_editar': usuario_editar,
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
    # Variable clave para saber si estamos editando
    ubicacion_editar = None

    # 1. Si la URL trae un 'editar_id', cargamos el objeto específico
    editar_id = request.GET.get('editar')
    if editar_id:
        ubicacion_editar = get_object_or_404(Ubicacion, pk=editar_id)

    if request.method == 'POST':
        nombre_ubi = request.POST.get('nombre_ubicacion')
        # Campo oculto en el formulario
        id_registro = request.POST.get('id_ubicacion')

        try:
            # SI TIENE ID, ESTAMOS ACTUALIZANDO (EDITAR)
            if id_registro:
                ubicacion_obj = get_object_or_404(Ubicacion, pk=id_registro)
                ubicacion_obj.nombre_ubicacion = nombre_ubi
                ubicacion_obj.save()
                success = "!Ubicación actualizada con éxito!"
            else:    
                if Ubicacion.objects.filter(nombre_ubicacion=nombre_ubi).exists():
                    error = "Esta ubicacion ya se encuentra registrado."
                else:
                    Ubicacion.objects.create(nombre_ubicacion=nombre_ubi)
                    success = "¡Ubicacion registrada con éxito¡"
            
            # Limpiamos la variable de edición tras guardar para que el formulario vuelva a modo "Crear"
            ubicacion_editar = None

        except Exception as e:
            error = f"Error técnico: {e}"

    # Obtenemos todas las ubicaciones para mostrarlas en una tabla resumen
    ubicaciones = Ubicacion.objects.all()

    context = {
        'ubicaciones': ubicaciones,
        # Se envía a la plantilla
        'ubicacion_editar': ubicacion_editar,
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
    estado_editar = None # Variable clave para saber si estamos editando

    edit_id = request.GET.get('editar')

    if edit_id:
        estado_editar = get_object_or_404(Estado, pk=edit_id)

    if request.method == 'POST':
        nombre_est = request.POST.get('nombre_estado')
        id_registro = request.POST.get('id_estado')

        try:
            if id_registro:
                estado_obj = get_object_or_404(Estado, pk=id_registro)
                estado_obj.nombre_estado = nombre_est
                estado_obj.save()
                success = "¡Ubicación actualizada con éxito!"
            else: 
                if Estado.objects.filter(nombre_estado=nombre_est).exists():
                    error = "Este estado ya se encuentra registrada."
                else:
                    Estado.objects.create(nombre_estado=nombre_est)
                    success = "¡Estado registrado con éxito!"

            estado_editar = None

        except Exception as e:
            error = f"Error técnico: {e}"

    # Obtenemos todas las ubicaciones para mostrarlas en una tabla resumen
    estados = Estado.objects.all()

    context = {
        'estados': estados,
        'estado_editar': estado_editar,
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
    # Variable clave para saber si estamos editando
    foto_editar = None

    # 1. Si la URL trae un 'editar_id', cargamos el objeto específico
    editar_id = request.GET.get('editar')

    if editar_id:
        foto_editar = get_object_or_404(Foto, pk=editar_id)

    if request.method == 'POST':
        nombre_img = request.POST.get('nombre_foto')
        # Capturamos el archivo adjunto desde el formulario
        archivo_imagen = request.FILES.get('archivo_imagen')

        id_registro = request.POST.get('id_foto')

        try:
            if id_registro:
                foto_obj = get_object_or_404(Foto, pk=id_registro)
                foto_obj.nombre_foto = nombre_img
                if archivo_imagen:
                    foto_obj.archivo = archivo_imagen
                foto_obj.save()
                success = "! Foto actualizada con éxito¡"
            else:
                if Foto.objects.filter(nombre_foto=nombre_img).exists():
                    error = "Esta Foto ya se encientra registrada."
                else:
                    Foto.objects.create(nombre_foto=nombre_img, archivo=archivo_imagen)
                    success = "¡Foto registrada con éxito!"
            
            foto_editar = None

        except Exception as e:
            error = f"Error técnico: {e}"

    # Obtenemos todas las Fotos para mostrarlas en una tabla resumen
    fotos = Foto.objects.all()

    context = {
        'fotos': fotos,
        'foto_editar': foto_editar,
        'error': error,
        'success': success,
        'nombre_usuario': request.session.get('nombre_usuario','Usuario'),
        'rol_usuario': request.session.get('rol','Invitado')
    }
    return render(request, 'gestion/foto.html', context)

def gestionar_bienes(request):
    error = None
    success = None
    #EDITAR
    bien_editar = None

    #EDITAR
    editar_id = request.GET.get('editar')

    if editar_id:
        bien_editar = get_object_or_404(Bien, pk=editar_id)

    if request.method == 'POST':
        # Capturamos los datos según los campos de tu modelo
        id_registro = request.POST.get('id_bien')
        nombre = request.POST.get('nombre_bien')
        descripcion = request.POST.get('descripcion')
        placa = request.POST.get('placa')
        id_ubi = request.POST.get('ubicacion')
        id_est = request.POST.get('estado')
        id_fot = request.POST.get('foto')

        try:
            # MODO EDITAR
            if id_registro:
                bien_obj = get_object_or_404(Bien, pk=id_registro)
                bien_obj.nombre_bien = nombre
                bien_obj.descripcion = descripcion
                bien_obj.placa = placa                
                bien_obj.id_ubicacion_id = id_ubi
                bien_obj.id_estado_id = id_est
                bien_obj.id_foto_id = id_fot
                bien_obj.save()
                success = "¡Bien actualizada con éxito!"
                bien_editar = None

            # MODO CREAR
            else:

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
        'bien_editar': bien_editar,
        'ubicaciones': ubicaciones,
        'estados': estados,
        'fotos': fotos,
        'error': error,
        'success': success,
        'nombre_usuario': request.session.get('nombre_usuario', 'Usuario'),
        'rol_usuario': request.session.get('rol','Invitado')
    }

    return render(request, 'gestion/bienes.html', context)                       
