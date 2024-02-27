from django.urls import path, include
from rest_framework import routers
from sistemaSolit import views
from . views import (
    LoginView,
    ProductosIndividualesView,
    upload_pdf,
    RepartoView
    )

router = routers.DefaultRouter()
router.register(r'Usuarios', views.UsuariosView, 'usuarios')
router.register(r'Prodcutos', views.ProductosView, 'productos')
router.register(r'Productos_indiviaduales', ProductosIndividualesView, 'productos_in')
router.register(r'Merma', views.MermaView, 'Merma')
router.register(r'Carretes', views.CarretesView, 'Carretes')
router.register(r'HistoricoView', views.HistoricoView, 'HistoricoView')
router.register(r'MaterialInstalacion', views.MaterialInstalacionView, 'MaterialInstalacion')
router.register(r'AlmacenSolitView', views.AlmacenSolitView, 'AlmacenSolitView')
router.register(r'Pedido', views.PedidoView, 'Pedido')
router.register(r'Alerta', views.AlertaView, 'Alerta')
router.register(r'ProductosTecnico', views.PermisosProductosTecnicoView, 'ProductosTecnico')
router.register(r'ProductosFucionador', views.PermisosProductosFucionadorView, 'ProductosFucionador')
router.register(r'ContratoFucionador', views.ContratosFucionadorView, 'ContratoFucionador')
reparto_list = RepartoView.as_view({
    'get': 'list',
    'post': 'create'
})

reparto_detail = RepartoView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
    'put': 'actualizar_nombre_administrador',
})
urlpatterns = [
    path("almacen", include(router.urls)),
   
    path('login/', LoginView.as_view()),
    path('upload-pdf/', upload_pdf),
    
    
     path('reparto/', reparto_list, name='reparto-list'),
    path('reparto/<int:pk>/', reparto_detail, name='reparto-detail'),
    
]