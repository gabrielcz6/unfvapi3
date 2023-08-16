from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=100)  
    urlfoto = models.CharField(null=True, max_length=500, blank=True)
    codigo = models.CharField(null=True, blank=True, max_length=100)  
    USER_TYPE_CHOICES = (
           ('student', 'Alumno'),
           ('teacher', 'Profesor'),
       )
   
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
   
class Escuela(models.Model):
    id_escuela = models.AutoField(primary_key=True)
    nombre_escuela = models.CharField(max_length=200)

class HoraDeMatricula(models.Model):
    idhoradematricula = models.AutoField(primary_key=True)
    dia_semana = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

class Curso(models.Model):
    codigo_curso = models.CharField(max_length=50, primary_key=True)
    nombre_curso = models.CharField(max_length=200)
    creditos = models.IntegerField()    
    profesor_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=1)

class Facultad(models.Model):
    id_facultad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    latitud = models.CharField(max_length=100) # Puede ser un campo PointField si se quiere guardar como geometría.    
    longitud = models.CharField(max_length=100) # Puede ser un campo PointField si se quiere guardar como geometría.    

class Matriculas(models.Model):
    idmatricula = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id_facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)
    codigo_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    id_escuela=models.ForeignKey(Escuela, on_delete=models.CASCADE)
    id_hora_de_matricula = models.ForeignKey(HoraDeMatricula, on_delete=models.CASCADE)
    año = models.IntegerField()
    ciclo = models.CharField(max_length=10)    

class Asistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_matricula = models.ForeignKey(Matriculas, on_delete=models.CASCADE)
    hora_registro = models.DateTimeField()
    asistio = models.BooleanField()
    latitud = models.CharField(max_length=100) # Puede ser un campo PointField si se quiere guardar como geometría.    
    longitud = models.CharField(max_length=100) # Puede ser un campo PointField si se quiere guardar como geometría.    
    urlfotoasistencia=models.CharField(default=0,max_length=500)
    

