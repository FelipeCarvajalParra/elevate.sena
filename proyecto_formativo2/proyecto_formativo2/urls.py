"""
URL configuration for proyecto_formativo2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from BD import views as BD_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Navegacion del usuario
    path('', core_views.index, name="Inicio"),
    path('inicio/', core_views.index, name="Inicio"),
    path('nosotros/', core_views.nosotros, name="Nosotros"),
    path('ubicacion/', core_views.ubicacion, name="Ubicacion"),
    path('registro/', core_views.registro, name="Registro"),
    #cursos
    path('trabajador_autorizado/', core_views.curso1, name="TrabajadorAutorizado"),
    path('reentrenamiento_sectorial/', core_views.curso2, name="ReentrenamientoSectorial"),
    path('coordinador/', core_views.curso3, name="Coordinador"),
    path('entrenador/', core_views.curso4, name="Entrenador"),
    path('actualizacion_coordinador/', core_views.curso5, name="ActualizacionCoordinador"),
    path('actualizacion_entrenador/', core_views.curso6, name="ActualizacionEntrenador"),
    

    # Crud mensajes
    path('mensajes/', core_views.mensajes, name="Mensajes"),
    path('RegistrarMensaje', BD_views.RegistrarMensaje, name="RegistrarMensaje"),
    path('Eliminar-Mensaje/<id>', BD_views.eliminarMensaje, name="EliminarMensaje"),

    # Administrador 
    #path('registros_cursos/<id_curso>', BD_views.registros_cursos, name="RegistrosCursos"),
    

    # Crud registro
    path("CrearRegistro/", BD_views.crearRegistro, name="CrearRegistro"),

    # inicio de sesion, y validacion de usuario (rol)
    path('accounts/', include('django.contrib.auth.urls')),
    path('redireccionarUsuario/', BD_views.redireccionar_usuario, name="redireccionarUsuario"),
    path('ingreso_aspirante', BD_views.redireccionar_usuario),

    #dashboard instructor
    path('dashboardInstructor/', BD_views.dashboard_instructor, name="DashboardInstructor"),
    path('cursos', BD_views.cursos, name="Cursos"),
    path('curso/<id>', BD_views.curso_fichas, name='curso/<id>'),
    path('mensajesRecibidos', BD_views.mensajes_recibidos, name="MensajesRecibidos"),
    
    
    #CRUD PERFIL INSTRUCTOR (no se elimina, ni se crea)
    path('perfilInstructor/', BD_views.perfil_instructor, name="PerfilInstructor"),
    path("actualizarInstructor/", BD_views.actualizar_instructor, name="ActualizarInstructor"),
    
    path('salir/', BD_views.cerrar_sesion, name="Salir"),
    
    #usuarios-admin
    path("usuariosRegistrados/", BD_views.usuarios_registrados, name="UsuariosRegistrados"),
    path("usuario/<documento>", BD_views.usuario_perfil_externo, name="UsuarioPerfil"),
    

    
    #Perfil aspirante
    path("inicioAspirante", BD_views.dashboard_aspirante, name="InicioAspirante"),
    path("listaFichas", BD_views.listar_fichas, name="ListaFichas"),
    path("perfilAspirante", BD_views.perfil_aspirante, name="PerfilAspirante"),
    path("actualizarAspirante", BD_views.actualizar_aspirante, name="ActualizarAspirante"),
    
    
    
    #CRUD FICHA
    path("agregarFicha/<ficha>/<curso>/<inicio>/<final>/<lugar>/<nota>", BD_views.crearFicha , name=""),
    path("actualizarFicha/<ficha_antigua>/<ficha_nueva>/<curso>/<inicio>/<final>/<lugar>/<nota>", BD_views.actualizarFicha , name=""),
    path("eliminarFicha/<ficha>/<curso>", BD_views.eliminarFicha , name="eliminarFicha/<ficha>/<curso>"),
    
    #CRUD FICHA_ASPIRANTE
    path("fichaAspirante/<curso>/<ficha>", BD_views.ficha, name="Ficha"),
    path("registroFichaAspirante/<ficha>/<usuario>", BD_views.crear_regitro_ficha_aspirante, name="RegistroFichaAspirante"),
    
    path("listarRegistros/", BD_views.listar_registros_fichas, name="ListarRegisrosFichas"),
    path("formularioActualizacion/<id>", BD_views.formulario_actualizacion_registro, name="FormularioActualizacion"),
    path("actualizarFichaAspirante/<id>", BD_views.actualizar_aspirante_ficha, name="ActualizarFichaAspirante"),
    
    #CRUD ASPIRANTE FICHA
    path("ficha/<ficha>", BD_views.aspirantesFicha, name="ficha/<ficha>"),
    path("eliminarRegistro/<id>/<ficha>", BD_views.eliminarAspiranteFicha, name="eliminarRegistro/<id>/<ficha>"),
    
    #crear archivo de excel
    path("crearExcel/<ficha>", BD_views.exportar_a_excel, name="crearExcel/<ficha>"),
    path("actualizarEstadoFicha/<estado>/<ficha>/<curso>", BD_views.estadoFicha, name="actualizarEstadoFicha/<estado>/<ficha>/<curso>")
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
