# tienda/urls.py
from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    # URLs públicas
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle'),
    
    # URLs de usuario
    path('perfil/', views.perfil, name='perfil'),
    
    # URLs de administración de productos
    path('admin/productos/', views.lista_admin_productos, name='admin_productos'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    
    # URLs de categorías
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
]