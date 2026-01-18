from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.timezone import now
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

from .models import Venta
from .forms import VentaForm

# LISTA
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista.html', {'ventas': ventas})

# AGREGAR
def agregar_venta(request):
    form = VentaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_ventas')
    return render(request, 'ventas/form.html', {'form': form})

# EDITAR
def editar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    if venta.cerrada:
        return redirect('lista_ventas')

    form = VentaForm(request.POST or None, instance=venta)
    if form.is_valid():
        form.save()
        return redirect('lista_ventas')
    return render(request, 'ventas/form.html', {'form': form})

# ELIMINAR
def eliminar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        return redirect('lista_ventas')
    return render(request, 'ventas/eliminar.html', {'venta': venta})

# CERRAR VENTA
def cerrar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)
    venta.cerrada = True
    venta.save()
    return redirect('lista_ventas')

# TICKET PDF (UNA VENTA)
def ticket_pdf(request, id):
    venta = get_object_or_404(Venta, id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{venta.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    contenido = [
        Paragraph("<b>TICKET DE VENTA</b>", styles['Title']),
        Paragraph(f"Producto: {venta.producto}", styles['Normal']),
        Paragraph(f"Cliente: {venta.cliente}", styles['Normal']),
        Paragraph(f"Cantidad: {venta.cantidad}", styles['Normal']),
        Paragraph(f"Precio unitario: ${venta.precio_unitario}", styles['Normal']),
        Paragraph(f"<b>TOTAL: ${venta.total}</b>", styles['Heading2']),
        Paragraph(f"Fecha: {venta.fecha}", styles['Normal']),
    ]

    doc.build(contenido)
    return response

# REPORTE DIARIO PDF
def reporte_diario_pdf(request):
    hoy = now().date()
    ventas = Venta.objects.filter(fecha__date=hoy, cerrada=True)

    total_dia = sum(v.total for v in ventas)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_diario.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)

    data = [['Producto', 'Cliente', 'Total']]
    for v in ventas:
        data.append([v.producto, v.cliente, v.total])

    data.append(['', 'TOTAL DEL DÍA', total_dia])

    doc.build([Table(data)])
    return response
