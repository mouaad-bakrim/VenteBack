from django.contrib import admin
from client.models import Client
from django.utils.safestring import mark_safe


class CLientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'type_client', 'date_creation', 'statut', 'site', 'entreprise_nom', 'SIRET', 'num_tva', 'utilisateur','qr_code_preview')
    list_filter = ('type_client', 'statut', 'site')
    search_fields = ('nom', 'email', 'telephone', 'entreprise_nom', 'SIRET', 'num_tva')
    readonly_fields = ('date_creation',)
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'email', 'telephone', 'type_client', 'statut', 'site', 'entreprise_nom', 'SIRET', 'num_tva', 'utilisateur')
        }),
        ('Création', {
            'fields': ('date_creation',),
            'classes': ('collapse',),
        }),
    )

    def qr_code_preview(self, obj):
        if obj.qr_code:
            return mark_safe(f'<img src="{obj.qr_code.url}" width="100" height="100" />')
        return "Pas de QR Code"

    qr_code_preview.short_description = "QR Code"

admin.site.register(Client, CLientAdmin)