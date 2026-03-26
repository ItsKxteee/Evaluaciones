from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Perfil


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Rol', {'fields': ('rol',)}),
    )


admin.site.register(Perfil)

