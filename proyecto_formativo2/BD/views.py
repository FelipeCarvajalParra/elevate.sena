from django.shortcuts import render, redirect, HttpResponse, redirect, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Mensaje, Aspirante, Instructor, Ficha, FichaAspirante
from django.contrib.auth.models import User, Group
from django.contrib import messages
from openpyxl import Workbook
from django.db import transaction
import os
from django.conf import settings


from django.contrib.auth.decorators import user_passes_test


def group_required(group_name, redirect_url='login'):
    def decorator(view_func):
        @user_passes_test(lambda u: u.groups.filter(name=group_name).exists(), login_url=redirect_url)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# Función para validar el rol del usuario 
@login_required
def redireccionar_usuario(request):
    if request.user.groups.filter(name='instructor').exists():
        return redirect('DashboardInstructor')
    elif request.user.groups.filter(name='aspirantes').exists():
        return redirect('InicioAspirante')
    else:
        return cerrar_sesion()
    
    
#Funciones aspirante 
@login_required
@group_required('aspirantes', redirect_url='Salir')
def dashboard_aspirante(request):
    aspirante = Aspirante.objects.get(docu_aspir = request.user.id)
    context = {
        'usuario': aspirante,
    }
    return render(request, 'dashboard_aspirante/inicio_aspirante.html', context)


@login_required
@group_required('aspirantes', redirect_url='Salir')
def listar_fichas(request):
    
    aspirante = Aspirante.objects.get(docu_aspir = request.user.id)
    fichas = Ficha.objects.all()
    curso_titulos = {
        1: "Trabajador autorizado",
        2: "Rentrenamiento sectorial",
        3: "Coordinador",
        4: "Entrenador",
        5: "Actualizacion coordinador",
        6: "Actualizacion entrenador",
    }
    
    for ficha in fichas:
        ficha.curso_nombre = curso_titulos.get(ficha.curs_ficha, "No encontrado")
    
    context = {
        'fichas': fichas,
        'cursos': curso_titulos,
        'usuario': aspirante,
    }
    return render(request, 'dashboard_aspirante/lista_fichas.html', context)

@login_required
@group_required('aspirantes', redirect_url='Salir')
def ficha(request, curso, ficha):
    
    aspirante = Aspirante.objects.get(docu_aspir = request.user.id)
    ficha = Ficha.objects.get(nume_ficha = ficha)

    context = {
        'usuario': aspirante,
        'ficha': ficha,
        'nombre_curso': curso,
    }
    
    return render(request, 'dashboard_aspirante/ficha.html', context)

@login_required
@group_required('aspirantes', redirect_url='Salir')
def crear_regitro_ficha_aspirante(request, ficha, usuario):
    
    ficha_id = ficha
    usuario_documento = get_object_or_404(Aspirante, pk=usuario)
    ficha = Ficha.objects.get(nume_ficha=ficha_id)
    
    if request.method == 'POST':
        nivel_educativo = request.POST.get('nivel_educativo')
        empleador = request.POST.get('empleador')
        cargo = request.POST.get('cargo')
        arl = request.POST.get('arl')
        area = request.POST.get('area')
        genero = request.POST.get('genero')

        cedula_ampliada = request.FILES.get('cedula_ampliada')
        examen_aptitud = request.FILES.get('examen_aptitud')
        pago_seguridad_social = request.FILES.get('pago_seguridad_social')
        requisitos_previos = request.FILES.get('requisitos_previos')

        # Inicializar el diccionario de datos
        data = {
            'nume_ficha1': get_object_or_404(Ficha, pk=ficha_id),
            'docu_aspir1': usuario_documento,
            'nive_aspir': nivel_educativo,
            'empl_aspir': empleador,
            'carg_aspir': cargo,
            'arl_aspir': arl,
            'area_aspir': area,
            'sect_aspir': genero,
            'doc0': requisitos_previos,
            'doc1': cedula_ampliada,
            'doc2': examen_aptitud,
            'doc3': pago_seguridad_social,
        }

        # Agregar campos adicionales dependiendo del curso
        if ficha.curs_ficha == 2:
            data['doc4'] = request.FILES.get('diploma_avanzado')
        elif ficha.curs_ficha == 3:
            data['doc4'] = request.FILES.get('certificado_curso')
            data['doc5'] = request.FILES.get('constancia_laboral')
        elif ficha.curs_ficha == 4:
            data['doc4'] = request.FILES.get('titulo_tecnologo')
            data['doc5'] = request.FILES.get('experiencia_seguridad')
            data['doc6'] = request.FILES.get('experiencia_alturas')
            data['doc7'] = request.FILES.get('certificado_avanzado')
            data['doc8'] = request.FILES.get('certificado_coordinador')
            data['doc9'] = request.FILES.get('certificado_andamios')
            data['doc10'] = request.FILES.get('certificado_respondiente')
            data['doc11'] = request.FILES.get('certificado_industrial')
        elif ficha.curs_ficha == 5:
            data['doc4'] = request.FILES.get('certificado_curso')
        elif ficha.curs_ficha == 6:
            data['doc4'] = request.FILES.get('certificado_curso')
            data['doc5'] = request.FILES.get('certificado_entrenador')

        ficha_aspirante = FichaAspirante(**data)
        ficha_aspirante.save()
        
        messages.success(request, '¡Su registro se guardo correctamente!')
        return redirect('ListaFichas') 

@login_required
@group_required('aspirantes', redirect_url='Salir')
def perfil_aspirante(request):
    aspirante = Aspirante.objects.get(docu_aspir = request.user.id)
    context = {
        'usuario': aspirante,
    }
    return render(request, 'dashboard_aspirante/perfil_aspirante.html', context)

@login_required
@group_required('aspirantes', redirect_url='Salir')
def actualizar_aspirante(request):
    usuario = Aspirante.objects.get(docu_aspir = request.user.id) 
    if request.method == 'POST':
        nuevo_correo = request.POST['correo_electronico']
        if nuevo_correo != usuario.corr_aspir:
            if User.objects.filter(email=nuevo_correo).exists():
                messages.error(request, 'El correo electrónico ingresado ya está en uso.')
                return redirect('PerfilAspirante')
            else:
                user = User.objects.get(id = request.user.id)
                user.email = nuevo_correo
                user.username = nuevo_correo
                user.save()
        
        usuario.pnom_aspir = request.POST['primer_nombre']
        usuario.snom_aspir = request.POST['segundo_nombre']
        usuario.pape_aspir = request.POST['primer_apellido']
        usuario.sape_aspir = request.POST['segundo_apellido']
        usuario.tdoc_aspir = request.POST['tipo_documento']
        usuario.corr_aspir = nuevo_correo  
        usuario.save()
    
    messages.success(request, 'Cambios guardados correctamente')
    return redirect('PerfilAspirante')

# Sección de navegación del admin (instructor)
@login_required
@group_required('instructor', redirect_url='Salir')
def dashboard_instructor(request):
    # Dashboard (página de inicio)
    
    totalMensajes = Mensaje.objects.count()
    totalFichas = Ficha.objects.count()
    totalUsuarios = User.objects.count() - 1
    totalRegistros = FichaAspirante.objects.count()
    
    listaMen = Mensaje.objects.all()
    listaReg = FichaAspirante.objects.all()
    
    contex = {
        'total_mensajes': totalMensajes,
        'total_fichas': totalFichas,
        'total_usuarios': totalUsuarios,
        'total_registros': totalRegistros,
        'mensaje_grupo': listaMen,
        'registro_grupo': listaReg, 
        'instructor': Instructor.objects.get(iden_instr = 1),
    }
    
    return render(request, 'dashboard_instructor/dashboard.html', contex)

@login_required
@group_required('instructor', redirect_url='Salir')
def perfil_instructor(request):
    
    ListaIns = Instructor.objects.get(iden_instr=1)
    
    contex = {
        'instructor': ListaIns
    }
    
    return render(request, 'dashboard_instructor/perfil.html', contex)

@login_required
@group_required('instructor', redirect_url='Salir')
def actualizar_instructor(request):
    
    instructor = Instructor.objects.get(iden_instr = 1)
    imagen_anterior = instructor.foto_instr.path if instructor.foto_instr else None

    instructor.nomb_instr = request.POST.get('nomb_instr')
    instructor.carg_instr = request.POST.get('carg_instr')
    instructor.corr_instr = request.POST.get('corr_instr')
    instructor.tele_instr = request.POST.get('tele_instr')
    instructor.ciud_instr = request.POST.get('ciud_instr')
    instructor.cent_instr = request.POST.get('cent_instr')
    instructor.resu_instr = request.POST.get('resu_instr')

    if request.FILES.get('foto_instr'):
        instructor.foto_instr = request.FILES.get('foto_instr')
        
        if imagen_anterior and os.path.exists(imagen_anterior):
            os.remove(imagen_anterior)

    instructor.save()
    
    messages.success(request, '¡Perfil actualizado correctamente!')
    return redirect('PerfilInstructor')

@login_required 
@group_required('instructor', redirect_url='Salir')
def cursos(request):
    
    ListaIns = Instructor.objects.get(iden_instr = 1)
    
    contex = {
        'instructor': ListaIns
    }
    return render(request, 'dashboard_instructor/cursos.html', contex)

#Listado de fichas por curso
@login_required
@group_required('instructor', redirect_url='Salir')
def curso_fichas(request, id):
    
    ListaIns = Instructor.objects.get(iden_instr = 1)
    
    curso_titulos = {
        "1": "Trabajador autorizado",
        "2": "Rentrenamiento sectorial",
        "3": "Coordinador",
        "4": "Entrenador",
        "5": "Actualizacion coordinador",
        "6": "Actualizacion entrenador",
    }

    nombre_curso = curso_titulos.get(id, "Curso no identificado")
    
    ListaFic = Ficha.objects.filter(curs_ficha=id)
    
    contex = {
        'instructor': ListaIns,
        'fichas': ListaFic, 
        'curso': id, 
        'nombre_curso': nombre_curso
    }
    
    return render(request, 'dashboard_instructor/curso_fichas.html', contex)

# Sección CRUD tabla mensajes (no se edita)
@login_required
@group_required('instructor', redirect_url='Salir')
def mensajes_recibidos(request):
    # Vista para listar los mensajes
    ListaMen = Mensaje.objects.all()
    ListaIns = Instructor.objects.get(iden_instr = 1)
    
    contex = {
        'mensaje_grupo': ListaMen,
        'instructor': ListaIns,
    }
    
    return render(request, 'dashboard_instructor/mensajes_recibidos.html', contex)


def RegistrarMensaje(request):
    # Vista que guarda los mensajes de los usuarios
    nombre_post = request.POST['nombres']
    apellidos_post = request.POST['apellidos']
    correo_post = request.POST['correo']
    mensaje_post = request.POST['mensaje']
    
    Mensaje.objects.create(
        nomb_mensa=nombre_post,
        apel_mensa=apellidos_post,
        corr_mensa=correo_post,
        mens_mensa=mensaje_post
    )
    
    messages.success(request, '¡Mensaje registrado correctamente!')
    return redirect('Mensajes')

@login_required
def eliminarMensaje(request, id):
    # Eliminar mensaje
    registroBorrar = Mensaje.objects.get(iden_mensa=id)
    registroBorrar.delete()
    
    messages.success(request, '¡Mensaje eliminado!')
    return redirect('MensajesRecibidos')

# Función para crear un registro de aprendiz
def crearRegistro(request):
    if request.method == 'POST':
        primer_nombre = request.POST['primer_nombre']
        segundo_nombre = request.POST['segundo_nombre']
        primer_apellido = request.POST['primer_apellido']
        segundo_apellido = request.POST['segundo_apellido']
        correo_electronico = request.POST['correo_electronico']
        genero = request.POST['genero']
        pais_nacimiento = request.POST['pais_nacimiento']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        tipo_documento = request.POST['tipo_documento']
        numero_documento = request.POST['numero_documento']

        # Verificar si ya existe un usuario con el mismo correo electrónico o número de documento
        if User.objects.filter(email=correo_electronico).exists(): 
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('Registro')
        elif User.objects.filter(id=numero_documento).exists():
            messages.error(request, 'El número de documento ya está registrado.')
            return redirect('Registro')
        else:
            # Crear el registro de Aspirante
            aspirante = Aspirante(
                docu_aspir=numero_documento,
                tdoc_aspir=tipo_documento,
                pnom_aspir=primer_nombre,
                snom_aspir=segundo_nombre,
                pape_aspir=primer_apellido,
                sape_aspir=segundo_apellido,
                gene_aspir=genero,
                pais_aspir=pais_nacimiento,
                fech_aspir=fecha_nacimiento,
                corr_aspir=correo_electronico,
            )
            aspirante.save()

            # Crear el usuario en la tabla User
            user = User.objects.create_user(
                id=numero_documento,
                username=correo_electronico,
                email=correo_electronico,
                password=numero_documento,
                first_name=primer_nombre,
                last_name=primer_apellido
            )
            
            # Añadir el usuario al grupo "aspirante"
            aspirante_group = Group.objects.get(name='aspirantes')
            user.groups.add(aspirante_group)

            # Mensaje de éxito
            messages.success(request, '¡Usuario creado exitosamente!')
            return redirect('Registro')
    else:
        messages.error(request, 'Error en el registro')
        return redirect('Registro')


#crud tabla fichas 
@login_required
@group_required('instructor', redirect_url='Salir')
def crearFicha(request,ficha, curso, inicio, final, lugar, nota):
    
    if Ficha.objects.filter(pk=ficha).exists():
        messages.error(request, f'La ficha {ficha} ya existe')
        return redirect(f'/curso/{curso}')
    else: 
        instr2_instance = Instructor.objects.get(iden_instr=1)
        nuevaFicha = Ficha.objects.create(
            nume_ficha=ficha, 
            curs_ficha=curso, 
            inic_ficha=inicio, 
            fina_ficha=final, 
            luga_ficha=lugar, 
            nota_ficha=nota,
            iden_instr2=instr2_instance,
        )
        messages.success(request, 'Ficha registrada correctamente')
        return redirect(f'/curso/{curso}')

@login_required
@group_required('instructor', redirect_url='Salir')
def actualizarFicha(request, ficha_antigua, ficha_nueva, curso, inicio, final, lugar, nota):
    try:
        with transaction.atomic():
            # Verificar si la nueva clave primaria ya existe
            if ficha_nueva != ficha_antigua and Ficha.objects.filter(nume_ficha=ficha_nueva).exists():
                messages.error(request, f'La ficha {ficha_nueva} ya existe')
                return redirect(f'/curso/{curso}')
            
            if ficha_nueva == ficha_antigua:
                id_registro = Ficha.objects.get(nume_ficha=ficha_antigua)
                id_registro.curs_ficha = curso
                id_registro.inic_ficha = inicio
                id_registro.fina_ficha = final
                id_registro.luga_ficha = lugar
                id_registro.nota_ficha = nota
                
                id_registro.save()
                messages.success(request, f'¡Ficha {ficha_antigua} actualizada!')
                return redirect(f'/curso/{curso}')

            # Obtener el registro antiguo
            ficha_antigua_registro = Ficha.objects.get(nume_ficha=ficha_antigua)

            # Crear un nuevo registro con la nueva clave primaria
            ficha_nueva_registro = Ficha(
                nume_ficha=ficha_nueva,
                curs_ficha=curso,
                inic_ficha=inicio,
                fina_ficha=final,
                luga_ficha=lugar,
                nota_ficha=nota,
                iden_instr2=ficha_antigua_registro.iden_instr2  # Copiar el valor del campo de clave foránea
            )
            ficha_nueva_registro.save()

            # Actualizar las referencias en la tabla FichaAspirante
            FichaAspirante.objects.filter(nume_ficha1=ficha_antigua).update(nume_ficha1=ficha_nueva_registro)

            # Eliminar el registro antiguo
            ficha_antigua_registro.delete()

            messages.success(request, f'¡Ficha {ficha_nueva} actualizada!')
        
        return redirect(f'/curso/{curso}')

    except Ficha.DoesNotExist:
        messages.error(request, f'La ficha {ficha_antigua} no existe')
        return redirect(f'/curso/{curso}')
    except Exception as e:
        messages.error(request, f'Error al actualizar la ficha: {e}')
        return redirect(f'/curso/{curso}')

@login_required
@group_required('instructor', redirect_url='Salir')
def estadoFicha(request, ficha, estado, curso):
    
    id_registro = Ficha.objects.get(nume_ficha=ficha)
    id_registro.ficha_activa = estado
    id_registro.save()
    
    messages.success(request, f'Estado actualizado')
    return redirect(f'/curso/{curso}')
                

@login_required
@group_required('instructor', redirect_url='Salir')
def eliminarFicha(request, ficha, curso):
    
    registros_fichas = FichaAspirante.objects.filter(nume_ficha1 = ficha)
    registros_fichas.delete()
    
    ficha_eliminar =  Ficha.objects.get(nume_ficha=ficha)
    ficha_eliminar.delete()
    
    messages.success(request, f'¡ficha {ficha} eliminada correctamente!')
    return redirect(f'/curso/{curso}')
    

#crud ficha_aspirante
@login_required
def aspirantesFicha(request, ficha):
    
    listaReg = FichaAspirante.objects.filter(nume_ficha1=ficha)
    ListaIns = Instructor.objects.get(iden_instr = 1)
    
    context = {
        'ficha': ficha,
        'registros': listaReg,
        'instructor': ListaIns,
    }
    
    return render(request, 'dashboard_instructor/registros_fichas.html', context)



def listar_registros_fichas(request):
    # Obtener el usuario actual
    usuario_actual = request.user
    user_id = usuario_actual.id
    
    registros = FichaAspirante.objects.filter(docu_aspir1=user_id)
    
    # Diccionario de cursos
    curso_titulos = {
        "1": "Trabajador autorizado",
        "2": "Rentrenamiento sectorial",
        "3": "Coordinador",
        "4": "Entrenador",
        "5": "Actualización coordinador",
        "6": "Actualización entrenador",
    }
    
    # Añadir el nombre del curso a cada registro
    for registro in registros:
        curso_numero = str(registro.nume_ficha1.curs_ficha)
        registro.nombre_curso = curso_titulos.get(curso_numero, "Curso desconocido")
    
    context = {
        'registros': registros,
    }
    
    return render(request, 'dashboard_aspirante/registros.html', context)


def formulario_actualizacion_registro(request, id):
    
    registro = get_object_or_404(FichaAspirante, iden_ficha_aspirante = id)
    
    context = {
        'registro': registro,
    }
    
    return render(request, 'dashboard_aspirante/registro.html', context)

def actualizar_aspirante_ficha(request, id):

    ficha_aspirante = FichaAspirante.objects.get(iden_ficha_aspirante=id)
    
    ficha_aspirante.nive_aspir = request.POST.get('nivel_educativo')
    ficha_aspirante.empl_aspir = request.POST.get('empleador')
    ficha_aspirante.carg_aspir = request.POST.get('cargo')
    ficha_aspirante.arl_aspir = request.POST.get('arl')
    ficha_aspirante.area_aspir = request.POST.get('area')
    ficha_aspirante.sect_aspir = request.POST.get('sector')
    
    ficha_aspirante.save()

    #eliminación y actualización de los documentos adjuntos
    doc0 = request.FILES.get('doc0')
    if doc0:
        if ficha_aspirante.doc0 and os.path.isfile(ficha_aspirante.doc0.path):
            os.remove(ficha_aspirante.doc0.path)
        ficha_aspirante.doc0 = doc0

    doc1 = request.FILES.get('doc1')
    if doc1:
        if ficha_aspirante.doc1 and os.path.isfile(ficha_aspirante.doc1.path):
            os.remove(ficha_aspirante.doc1.path)
        ficha_aspirante.doc1 = doc1

    doc2 = request.FILES.get('doc2')
    if doc2:
        if ficha_aspirante.doc2 and os.path.isfile(ficha_aspirante.doc2.path):
            os.remove(ficha_aspirante.doc2.path)
        ficha_aspirante.doc2 = doc2

    doc3 = request.FILES.get('doc3')
    if doc3:
        if ficha_aspirante.doc3 and os.path.isfile(ficha_aspirante.doc3.path):
            os.remove(ficha_aspirante.doc3.path)
        ficha_aspirante.doc3 = doc3

    doc4 = request.FILES.get('doc4')
    if doc4:
        if ficha_aspirante.doc4 and os.path.isfile(ficha_aspirante.doc4.path):
            os.remove(ficha_aspirante.doc4.path)
        ficha_aspirante.doc4 = doc4

    doc5 = request.FILES.get('doc5')
    if doc5:
        if ficha_aspirante.doc5 and os.path.isfile(ficha_aspirante.doc5.path):
            os.remove(ficha_aspirante.doc5.path)
        ficha_aspirante.doc5 = doc5

    doc6 = request.FILES.get('doc6')
    if doc6:
        if ficha_aspirante.doc6 and os.path.isfile(ficha_aspirante.doc6.path):
            os.remove(ficha_aspirante.doc6.path)
        ficha_aspirante.doc6 = doc6

    doc7 = request.FILES.get('doc7')
    if doc7:
        if ficha_aspirante.doc7 and os.path.isfile(ficha_aspirante.doc7.path):
            os.remove(ficha_aspirante.doc7.path)
        ficha_aspirante.doc7 = doc7

    doc8 = request.FILES.get('doc8')
    if doc8:
        if ficha_aspirante.doc8 and os.path.isfile(ficha_aspirante.doc8.path):
            os.remove(ficha_aspirante.doc8.path)
        ficha_aspirante.doc8 = doc8

    doc9 = request.FILES.get('doc9')
    if doc9:
        if ficha_aspirante.doc9 and os.path.isfile(ficha_aspirante.doc9.path):
            os.remove(ficha_aspirante.doc9.path)
        ficha_aspirante.doc9 = doc9

    doc10 = request.FILES.get('doc10')
    if doc10:
        if ficha_aspirante.doc10 and os.path.isfile(ficha_aspirante.doc10.path):
            os.remove(ficha_aspirante.doc10.path)
        ficha_aspirante.doc10 = doc10

    doc11 = request.FILES.get('doc11')
    if doc11:
        if ficha_aspirante.doc11 and os.path.isfile(ficha_aspirante.doc11.path):
            os.remove(ficha_aspirante.doc11.path)
        ficha_aspirante.doc11 = doc11

    ficha_aspirante.save()

    messages.success(request, '¡Registro actualizado correctamente!')
    return redirect('/listarRegistros/')

    

@login_required
def eliminarAspiranteFicha(request, id, ficha):
    
    registro_eliminar = get_object_or_404(FichaAspirante, iden_ficha_aspirante=id)
    
    i = 0
    
    # Lista de los nombres de los campos de documentos
    campos_documentos = [f'doc{i}' for i in range(12)]
    
    # Eliminar archivos si existen
    for campo in campos_documentos:
        archivo = getattr(registro_eliminar, campo)
        if archivo and archivo.name:  # Verificamos si el archivo existe
            ruta_documento = os.path.join(settings.MEDIA_ROOT, archivo.name)
            if os.path.exists(ruta_documento):
                os.remove(ruta_documento)
    
    # Eliminar el registro
    registro_eliminar.delete()
    
    messages.success(request, '¡Registro eliminado correctamente!')
    return redirect(f'/ficha/{ficha}')


@login_required
@group_required('instructor', redirect_url='Salir')
def usuarios_registrados(request):
    
    aspirantes = Aspirante.objects.all()
    ListaIns = Instructor.objects.get(iden_instr = 1)
    
    contex = {
        'aspirantes': aspirantes, 
        'instructor': ListaIns,
    }
    
    return render(request, 'dashboard_instructor/usuarios.html', contex)


@login_required
@group_required('instructor', redirect_url='Salir')
def usuario_perfil_externo(request, documento):
    
    usuario = get_object_or_404(Aspirante, docu_aspir = documento)
    ListaIns = Instructor.objects.get(iden_instr = 1)
    
    contex = {
        'usuario': usuario, 
        'instructor': ListaIns,
    }
    
    return render(request, 'dashboard_instructor/usuario_perfil.html', contex)

@login_required
@group_required('instructor', redirect_url='Salir')
def exportar_a_excel(request, ficha):
    # Filtra los registros según la llave foránea aspirante_id
    registros = FichaAspirante.objects.filter(nume_ficha1=ficha)
    numero_registros = registros.count()
    
    if numero_registros == 0:
        messages.error(request, f"La ficha {ficha} no tiene registros")
        return redirect(f'/ficha/{ficha}')
    else:
        # Crea un nuevo libro de trabajo
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = f'{ficha}'

        # Escribe la cabecera
        headers = ["tipo_documento", "documento", "priner nombre", "segundo nombre", "primer apellido", "segundo apellido",	"genero", "pais nacimiento", "fecha nacimiento", "nivel educativo", 'area de trabajo', 'cargo actual', 'SECTOR', 'EMPLEADOR', 'ARL']
        worksheet.append(headers)

        # Escribe los datos
        for registro in registros:
            row = [
                registro.docu_aspir1.tdoc_aspir,
                registro.docu_aspir1.docu_aspir,
                registro.docu_aspir1.pnom_aspir,
                registro.docu_aspir1.snom_aspir,
                registro.docu_aspir1.pape_aspir,
                registro.docu_aspir1.sape_aspir,
                registro.docu_aspir1.gene_aspir,
                registro.docu_aspir1.pais_aspir,
                registro.docu_aspir1.fech_aspir,
                registro.nive_aspir,
                registro.area_aspir,
                registro.carg_aspir,
                registro.sect_aspir,
                registro.empl_aspir,
                registro.arl_aspir
            ]
            worksheet.append(row)
            
        for column_cells in worksheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

        # Configura la respuesta HTTP
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=ReporteFicha_{ficha}.xlsx'

        # Guarda el archivo Excel en la respuesta
        workbook.save(response)

        return response

# Función para cerrar sesión 
def cerrar_sesion(request):
    logout(request)
    return redirect('/inicio')



