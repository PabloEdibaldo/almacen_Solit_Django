from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'clientes', views.Clientes_ViewSet,'Clientes')
router.register(r'facturacion', views.Clientes_ViewSet,'Facturacion')
router.register(r'inpuestos', views.Clientes_ViewSet,'inpuestos')
router.register(r'notificacion', views.Clientes_ViewSet,'Notificacion')
router.register(r'instalacion', views.Instalcion_ViewSet,'instalacion')

urlpatterns = [
    path('', include(router.urls)),
]
