from django.urls import path, include
from rest_framework import routers
from sistemaSolit import views
from . views import (
    LoginView,
    ProductosIndividualesView,
    upload_pdf,
    RepartoView,
    LogoutView,
    get_pedidos_by_pdf,
    devolucionProducto,
    crearProductosPorCodigoDeBarras,
    sacarMaterialPorCodigoBarras
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
router.register(r'ZonasUsoMaterial', views.ZonasusoMaterialView, 'ZonasUsoMaterial')
router.register(r'Calendario', views.CalendarioView, 'Calendario')
router.register(r'NombrePdfsSubidosView', views.NombrePdfsSubidosView, 'NombrePdfsSubidosView')

router.register(r'ProductosPrestadosView', views.ProductosPrestadosView, 'ProductosPrestadosView    ')

router.register(r'Devoluciones', views.DevolucionesView, 'Devoluciones    ')


router.register(r'AuditLogView', views.AuditLogView, 'AuditLogView')
router.register(r'ZonaAlmacen', views.ZonasAlmacenView, 'ZonaAlmacen')

router.register(r'UsoProductoView', views.UsoProductoView, 'UsoProductoView')


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
   
    
    
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
    path('upload-pdf/', upload_pdf),
    path('devolucionProducto/', devolucionProducto),
    path('crearProductosPorCodigoDeBarras/', crearProductosPorCodigoDeBarras),
    path('sacarMaterialPorCodigoBarras/', sacarMaterialPorCodigoBarras),


    
    
    
    path('reparto/', reparto_list, name='reparto-list'),
    path('reparto/<int:pk>/', reparto_detail, name='reparto-detail'),
    path('subir-img/<int:producto_id>/', views.AgregarImagenProducto.as_view() ),
    path('pedidos/<int:pdf_id>/', get_pedidos_by_pdf, name='get_pedidos_by_pdf'),

]