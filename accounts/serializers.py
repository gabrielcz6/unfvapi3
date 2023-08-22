# serializers.py
from rest_framework import serializers
from .models import Curso,CustomUser,Asistencia,Matriculas
from datetime import datetime

class CursoNombreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['codigo_curso', 'nombre_curso', 'creditos','profesor_id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'codigo')




class AsistenciaSerializer(serializers.ModelSerializer):
    codigo_estudiante = serializers.CharField(write_only=True)
    codigo_curso = serializers.CharField(write_only=True)

    class Meta:
        model = Asistencia
        fields = ('codigo_estudiante', 'codigo_curso', 'hora_registro', 'asistio', 'latitud', 'longitud', 'urlfotoasistencia')

    def create(self, validated_data):
        codigo_estudiante = validated_data.pop('codigo_estudiante')
        codigo_curso = validated_data.pop('codigo_curso')
        user = CustomUser.objects.get(codigo=codigo_estudiante)
        matricula = Matriculas.objects.filter(id_usuario=user, codigo_curso__codigo_curso=codigo_curso).first()
        if matricula is None:
            raise serializers.ValidationError(f"No se encontró la matrícula para el estudiante con código {codigo_estudiante} y curso {codigo_curso}")
        validated_data['hora_registro'] = datetime.now().isoformat()
        return Asistencia.objects.create(id_matricula=matricula, **validated_data)


class AsistenciaporcursoSerializer(serializers.ModelSerializer):
    nombre_usuario = serializers.CharField(source='id_matricula.id_usuario.name')
    urlfotoasistencia = serializers.CharField()
    fecha_hora_asistencia = serializers.DateTimeField(source='hora_registro', format='%Y-%m-%d %I:%M %p')
    coordenada_x = serializers.CharField(source='latitud')
    coordenada_y = serializers.CharField(source='longitud')

    class Meta:
        model = Asistencia
        fields = ('nombre_usuario', 'urlfotoasistencia', 'fecha_hora_asistencia', 'coordenada_x', 'coordenada_y')


