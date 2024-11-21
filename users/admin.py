from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Worker Info', {'fields': ('is_worker', 'is_admin', 'can_add_stock', 'can_add_order')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_worker', 'is_admin', 'can_add_stock', 'can_add_order')}
        ),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_worker', 'is_admin', 'can_add_stock', 'can_add_order')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
