from django.urls import path
from . import views
urlpatterns = [
    path('', views.lista_ventas, name='lista_ventas'),
    path('agregar/', views.agregar_venta, name='agregar_venta'),
    path('editar/<int:id>/', views.editar_venta, name='editar_venta'),
    path('eliminar/<int:id>/', views.eliminar_venta, name='eliminar_venta'),

    path('cerrar/<int:id>/', views.cerrar_venta, name='cerrar_venta'),
    path('ticket/<int:id>/', views.ticket_pdf, name='ticket_pdf'),
    path('reporte-diario/', views.reporte_diario_pdf, name='reporte_diario_pdf'),
]

