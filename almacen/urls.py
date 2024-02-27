from django.urls import path,include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'proveedor_almacen',views.Proveedor_view,'Proveedor_almacen')
router.register(r'accesorio_almacen',views.Accesorio_view,'Accesorio_almacen')
router.register(r'Producto_almacen',views.Producto_view,'Producto_almacen')
router.register(r'tecnico_almacen',views.Tecnico_view,'Tecnico_almacen')
router.register(r'Instalacion_almacen',views.Insta_view,'Instalacion_almacen')
router.register(r'productosinstalacion',views.ProductosInstalacion_view,'productosinstalacion')

router.register(r'Instalacion',views.InstalacionViewSet,'Instalacion')

urlpatterns = [
    path('',include(router.urls)),

]
