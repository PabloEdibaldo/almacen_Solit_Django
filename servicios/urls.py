from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'ServiciosInternet',views.ServiciosInternet_View,'ServiciosInternet')
router.register(r'Serviciostelefonicos',views.ServicioTelefonico_View,'Serviciostelefonicos')
router.register(r'Serviciospersonalizados',views.ServiciosPersonalizados_View,'serviciospersonalizados')

urlpatterns = [
    path('', include(router.urls)),
]
