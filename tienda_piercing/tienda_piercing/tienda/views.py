# tienda/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Producto, Categoria, Pedido, DetallePedido
from .forms import ProductoForm, CategoriaForm

def inicio(request):
    productos_destacados = Producto.objects.filter(activo=True)[:8]
    categorias = Categoria.objects.all()
    return render(request, 'tienda/inicio.html', {
        'productos': productos_destacados,
        'categorias': categorias
    })

def lista_productos(request):
    productos = Producto.objects.filter(activo=True)
    categorias = Categoria.objects.all()
    
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    return render(request, 'tienda/productos.html', {
        'productos': productos,
        'categorias': categorias
    })

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    return render(request, 'tienda/detalle.html', {
        'producto': producto
    })

@login_required
def perfil(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha_pedido')
    return render(request, 'tienda/perfil.html', {
        'pedidos': pedidos
    })

# Nuevas vistas para gestión de productos
@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('tienda:detalle', producto_id=producto.id)
        else:
            messages.error(request, 'Hubo errores en el formulario. Por favor, corrígelos.')
    else:
        form = ProductoForm()
    
    return render(request, 'tienda/crear_producto.html', {
        'form': form,
        'titulo': 'Crear Nuevo Producto'
    })

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('tienda:detalle', producto_id=producto.id)
        else:
            messages.error(request, 'Hubo errores en el formulario. Por favor, corrígelos.')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'tienda/crear_producto.html', {
        'form': form,
        'producto': producto,
        'titulo': f'Editar Producto: {producto.nombre}'
    })

@login_required
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('tienda:crear_producto')
        else:
            messages.error(request, 'Hubo errores en el formulario. Por favor, corrígelos.')
    else:
        form = CategoriaForm()
    
    return render(request, 'tienda/crear_categoria.html', {
        'form': form,
        'titulo': 'Crear Nueva Categoría'
    })

@login_required
def lista_admin_productos(request):
    """Vista para que los administradores vean todos los productos"""
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'tienda/admin_productos.html', {
        'productos': productos
    })

@login_required
def eliminar_producto(request, producto_id):
    """Vista para eliminar un producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('tienda:admin_productos')
    
    return render(request, 'tienda/confirmar_eliminacion.html', {
        'producto': producto
    })