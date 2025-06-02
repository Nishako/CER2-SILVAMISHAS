from django.db import models
from django.contrib.auth.models import User

MATERIALES = [
    ('PAP', 'Papel y cartón'),
    ('PLAS', 'Plásticos reciclables'),
    ('VID', 'Vidrios'),
    ('LAT', 'Latas'),
    ('ELEC', 'Electrónicos pequeños'),
    ('TEX', 'Textiles'),
    ('VOL', 'Voluminosos reciclables'),
]

ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('en_ruta', 'En ruta'),
    ('completada', 'Completada'),
]

class Solicitud(models.Model):
    ciudadano = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_material = models.CharField(max_length=10, choices=MATERIALES)
    cantidad = models.IntegerField()
    fecha_estimada = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    comentario_operario = models.TextField(blank=True, null=True)
    operario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignadas')
    
    def __str__(self):
        return f"Solicitud de {self.ciudadano.username} - {self.tipo_material}"
