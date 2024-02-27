
from django.urls import path,include 
from . views import (Datos_Clientes_PPP_View,
                    Datos_ClientesView,
                    Datos_RouterView,
                    RouterView,
                    ZonasView,
                    ProfilesView,
                    Redes_ipb4View,
                    MonitoreoView,
                    NapCajaView,
                    obtenerClientesSmartOLT,
                    ObtenerVLANs,
                    GetRoutingCofig,
                    GetONUfullStatus,
                    getTrafficGrap,
                    getSignalGraph,
                    )
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'Routers', RouterView,'Routers')
router.register(r'redes_ipv4',Redes_ipb4View,'Redes_ipv4')
router.register(r'Monitoreo',MonitoreoView,'monitoreo')
router.register(r'CajaNap',NapCajaView,'cajaNap')

urlpatterns = [
    path('datos_cli_PPP/', Datos_Clientes_PPP_View.as_view(), name='Datos del cliente PPP'),
    path('datos_cli/', Datos_ClientesView.as_view(), name='Datos del cliente'),
    path('datos_rout/', Datos_RouterView.as_view(), name='Datos del router'),
    path('',include(router.urls)),
    path('olt/get_zones/', ZonasView.as_view(), name='gest zones'),
    # path('olt/post_zones/', ZonasView.as_view(), name='post zones'),
    path('olt/get_profiles/', ProfilesView.as_view(), name='gest zones'),
    path('olt/data/', obtenerClientesSmartOLT.as_view(), name='olts'),
    path('olt/vlans/',ObtenerVLANs.as_view(),name='vlans en la olt'),
    path('olt/get-onu-status/', GetONUfullStatus.as_view()),
    path('olt/get-rounting-config/', GetRoutingCofig.as_view()),
    path('olt/get-traffic-grap/', getTrafficGrap.as_view()),
    path('olt/get-onu-signal-grap/', getSignalGraph.as_view()),
 


]
