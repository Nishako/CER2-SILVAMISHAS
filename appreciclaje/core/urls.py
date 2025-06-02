from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('solicitud/nueva/', views.nueva_solicitud, name='nueva'),
    path('solicitud/historial/', views.historial, name='historial'),
    path('registro/', views.registro, name='registro'),
    path('materiales/', views.info_materiales, name='materiales'),
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    path('puntos-limpios/', views.puntos_limpios, name='puntos_limpios'),
    path('metricas/', views.metricas, name='metricas'),
    path('operario/', views.gestion_operario, name='operario'),
]
