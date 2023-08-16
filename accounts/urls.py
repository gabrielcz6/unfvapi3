# posts/urls.py
from django.urls import path
from .views import ImageView, CursosEstudianteView,RegistrarAsistenciaView,CursoList,UsuariosMatriculadosEnCurso,AsistenciaPorCurso # new

urlpatterns = [
 path('uploadimage/', ImageView.as_view(), name='file_upload'),
 path('cursos-estudiante/<str:codigo_estudiante>/', CursosEstudianteView.as_view(), name='cursos-estudiante'),
 path('registrar_asistencia/', RegistrarAsistenciaView.as_view(), name='registrar-asistencia'),
 path('cursos/', CursoList.as_view(), name='curso-list'),
 path('curso/<str:codigo_curso>/matriculas/', UsuariosMatriculadosEnCurso.as_view(), name='usuarios-matriculados'),
 path('asistencias/<str:codigo_curso>/<str:fecha_inicio>/<str:fecha_fin>/', AsistenciaPorCurso.as_view(),name="asistencia-curso")
 # urls.py

]