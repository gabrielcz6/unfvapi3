# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Asistencia,Curso,Facultad,HoraDeMatricula,Matriculas,Escuela

class HoraDeMatriculaAdmin(admin.ModelAdmin):
    list_display = ('idhoradematricula', 'dia_semana', 'hora_inicio', 'hora_fin')
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ('idhoradematricula', 'dia_semana', 'hora_inicio', 'hora_fin')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ('idhoradematricula', 'dia_semana', 'hora_inicio', 'hora_fin')}),)  

class CustomUserAdmin(UserAdmin):
   add_form = CustomUserCreationForm
   form = CustomUserChangeForm
   model = CustomUser
   list_display = [
                  "email",
                  "username",
                  "name",
                  "is_staff",
                  "urlfoto",
                  "codigo",
                  "user_type",
                     ]
   fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("name","urlfoto","codigo","user_type")}),)
   add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("name","urlfoto","codigo","user_type")}),)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(HoraDeMatricula)
admin.site.register(Curso)
admin.site.register(Facultad)
admin.site.register(Matriculas)
admin.site.register(Asistencia)
admin.site.register(Escuela)