from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username','email', 'role','is_active')
    ordering = ('-date_joined', )
    filter_horizontal = ()
    fieldsets = ()
    list_filter = ()

admin.site.register(User,CustomAdmin)
admin.site.register(UserProfile)