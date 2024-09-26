from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type', 'endereco_codename')
    search_fields = ('name', 'codename')

    def endereco_codename(self, obj):
        return f"{obj.content_type.app_label}.{obj.codename}"
    endereco_codename.short_description = 'Endereço do Codename'
