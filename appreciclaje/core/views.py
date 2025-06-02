from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import SolicitudForm
from .models import Solicitud
from django.contrib.auth import login
from .forms import RegistroForm
from django.db.models import Count, Avg
from datetime import datetime
from django.db import models

def inicio(request):
    return render(request, 'core/index.html')

@login_required
def nueva_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.ciudadano = request.user
            solicitud.save()
            return redirect('historial')
    else:
        form = SolicitudForm()
    return render(request, 'core/nueva_solicitud.html', {'form': form})

@login_required
def historial(request):
    solicitudes = Solicitud.objects.filter(ciudadano=request.user)
    return render(request, 'core/historial.html', {'solicitudes': solicitudes})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('nueva')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})

def info_materiales(request):
    materiales = [
        ('PAP', 'Papel y cartón', 'Incluye cajas, hojas, periódicos, cuadernos (sin espirales ni plásticos).'),
        ('PLAS', 'Plásticos reciclables', 'Botellas PET, envases de alimentos, tapas plásticas. No se aceptan bolsas ni film.'),
        ('VID', 'Vidrios', 'Botellas y frascos sin tapa. No se reciben vidrios rotos ni espejos.'),
        ('LAT', 'Latas', 'Latas de aluminio y hojalata, como bebidas o conservas.'),
        ('ELEC', 'Electrónicos pequeños', 'Celulares, tablets, teclados, cargadores. No se aceptan refrigeradores ni TV.'),
        ('TEX', 'Textiles', 'Ropa en buen estado, sábanas, cortinas. No se aceptan prendas sucias o rotas.'),
        ('VOL', 'Voluminosos reciclables', 'Muebles, colchones, bicicletas, palets.'),
    ]
    return render(request, 'core/materiales.html', {'materiales': materiales})

def recomendaciones(request):
    return render(request, 'core/recomendaciones.html')

def puntos_limpios(request):
    return render(request, 'core/puntos_limpios.html')

def metricas(request):
    solicitudes_por_mes = (
        Solicitud.objects
        .extra({'mes': "strftime('%%Y-%%m', fecha_estimada)"})
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    materiales_populares = (
        Solicitud.objects
        .values('tipo_material')
        .annotate(total=Count('tipo_material'))
        .order_by('-total')[:5]
    )

    solicitudes = Solicitud.objects.all()
    if solicitudes.exists():
        suma_dias = 0
        for s in solicitudes:
            diferencia = (date.today() - s.fecha_estimada).days
            suma_dias += abs(diferencia)
        promedio_dias = round(suma_dias / solicitudes.count())
    else:
        promedio_dias = None

    return render(request, 'core/metricas.html', {
        'solicitudes_por_mes': solicitudes_por_mes,
        'materiales_populares': materiales_populares,
        'promedio_dias': promedio_dias['promedio'],
    })

def es_operario(user):
    return user.groups.filter(name='operario').exists()

@login_required
@user_passes_test(es_operario)
def gestion_operario(request):
    solicitudes = Solicitud.objects.filter(operario=request.user)

    if request.method == 'POST':
        solicitud_id = request.POST.get('id')
        nuevo_estado = request.POST.get('estado')
        comentario = request.POST.get('comentario')

        solicitud = Solicitud.objects.get(id=solicitud_id, operario=request.user)
        solicitud.estado = nuevo_estado
        solicitud.comentario_operario = comentario
        solicitud.save()

    return render(request, 'core/gestion_operario.html', {'solicitudes': solicitudes})
