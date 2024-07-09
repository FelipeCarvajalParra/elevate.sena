from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.contrib.auth import logout

def index(request): #pagina principa 
    return render(request, 'index.html')

def curso1(request): #curso trabajador autorizado
    return render(request, 'curso1.html')

def curso2(request): #curso reentrenamiento sectorial
    return render(request, 'curso2.html')

def curso3(request): #curso coordinador
    return render(request, 'curso3.html')

def curso4(request): #curso entrenador
    return render(request, 'curso4.html')

def curso5(request): #curso actualizacion de coordinador
    return render(request, 'curso5.html')

def curso6(request): #curso actualizacion de entrenador
    return render(request, 'curso6.html')

def nosotros(request): #pagina nosotros
    return render(request, 'nosotros.html')

def mensajes(request): #pagina de mensajes
    return render(request, 'mensajes.html')

def ubicacion(request): #pagina de ubicacion
    return render(request, 'ubicacion.html')

def registro(request): #pagina de registro a los cursos 
    return render(request, 'registro.html')






