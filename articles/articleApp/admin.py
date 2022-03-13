from curses.ascii import US
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.

# TokenAdmin.raw_id_fields = ['user']

class UserAdminCustomised(UserAdmin):
    list_filter = ('admin', 'staff')

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Added Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'university_id',
                    'phone',
                    'rule',
                    'is_admin',
                    'is_confirmed'
                ),
            },
        ),
    )

class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(User,UserAdminCustomised)
admin.site.register(Log,LogAdmin)
admin.site.register(Book)
admin.site.register(Facultie)
admin.site.register(Department)
admin.site.register(SubjectCode)


