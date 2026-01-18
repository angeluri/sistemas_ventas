from django.contrib import admin
from .models import Venta

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'producto',
        'cliente',
        'cantidad',
        'precio_unitario',
        'total',
        'cerrada',
        'fecha'
    )

    list_filter = ('cerrada', 'fecha')
    search_fields = ('producto', 'cliente')
    ordering = ('-fecha',)

    readonly_fields = ('total', 'fecha')

    list_editable = ('cerrada',)

    def has_change_permission(self, request, obj=None):
        if obj and obj.cerrada:
            return False
        return True
