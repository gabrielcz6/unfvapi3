from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.utils import timezone
import io
import base64
from PIL import Image,ExifTags
import requests
from .utils import get_image_from_firebase, compare_images
# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import Asistencia, Matriculas, CustomUser, Curso
from .serializers import CursoNombreSerializer,AsistenciaSerializer,UserSerializer,AsistenciaSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers,generics, status





class ImageView(APIView):
    # input("tumama")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        
          codigo_provided = request.data.get('codigo')  # Asume que el código se envía en el cuerpo de la solicitud
          try:
              user = CustomUser.objects.get(codigo=codigo_provided) # Asume que 'codigo' es un campo en tu modelo de Usuario
          except User.DoesNotExist:
              return Response({'status': 'Código no válido'}, status=status.HTTP_400_BAD_REQUEST)
        
        
          image_received = request.POST.get('image')
          print(type(image_received))
          image_temp=base64.b64decode(image_received)
          image_temp=io.BytesIO(image_temp)
          image_temp = Image.open(image_temp)
          image_temp.save('temp_imagerequest.jpg')
          ## Descargar la imagen de Firebase
          image_url = request.user.urlfoto
          response = requests.get(image_url)
          #data = io.BytesIO(response.content)
          data=io.BytesIO(response.content)
          # Abrir los bytes como una imagen
          image2 = Image.open(data)
          try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image2._getexif().items())
  
            if exif[orientation] == 3:
                image2 = image2.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image2 = image2.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image2 = image2.rotate(90, expand=True)
          except (AttributeError, KeyError, IndexError):
          # Las imágenes antiguas o las que no son de una cámara pueden no tener datos Exif
            pass
          puntaje=(compare_images(image_temp, image2))
          #print(puntaje)
          if puntaje>0.95:
                   status = "verificado con :"+ str(round(puntaje * 100, 1)) + "%"
                   return Response({'status': status})
          else:
                   status = 0
                   return Response({'status': status})
          

class CursosEstudianteView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, codigo_estudiante, *args, **kwargs):
        
        user = get_object_or_404(get_user_model(), codigo=codigo_estudiante)
        matriculas = Matriculas.objects.filter(id_usuario=user)
        cursos = [matricula.codigo_curso for matricula in matriculas.all()]

        serializer = CursoNombreSerializer(cursos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)      
   
  

class RegistrarAsistenciaView(generics.CreateAPIView):
    serializer_class = AsistenciaSerializer

class CursoList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    queryset = Curso.objects.all()
    serializer_class = CursoNombreSerializer



class UsuariosMatriculadosEnCurso(generics.ListAPIView):
     serializer_class = UserSerializer
 
     def get_queryset(self):
         codigo_curso = self.kwargs['codigo_curso']
         curso = Curso.objects.get(codigo_curso=codigo_curso)
         matriculas = Matriculas.objects.filter(codigo_curso=curso)
         usuarios = [matricula.id_usuario for matricula in matriculas]
         return CustomUser.objects.filter(id__in=[usuario.id for usuario in usuarios])
     
class AsistenciaPorCurso(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, codigo_curso, fecha_inicio, fecha_fin):
        fecha_inicio = timezone.datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_fin = timezone.datetime.strptime(fecha_fin, "%Y-%m-%d")

        matriculas_curso = Matriculas.objects.filter(codigo_curso__codigo_curso=codigo_curso)
        asistencias = Asistencia.objects.filter(
            id_matricula__in=matriculas_curso,
            hora_registro__range=(fecha_inicio, fecha_fin)
        )

        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response(serializer.data)