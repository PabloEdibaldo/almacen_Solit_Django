from rest_framework import generics
from rest_framework import viewsets
from .models import (
    ServiciosInternet,
    ServicioTelefonico,
    ServiciosPersonalizados
)
from .serializers import (
    ServicioInternet_serializers,
    ServicioTelefonico_serializers,
    ServicioPersonalizados_serializers
)
class ServiciosInternet_View(viewsets.ModelViewSet):
    serializer_class = ServicioInternet_serializers
    queryset = ServiciosInternet.objects.all()


class ServicioTelefonico_View(viewsets.ModelViewSet):
    serializer_class = ServicioTelefonico_serializers
    queryset = ServicioTelefonico.objects.all()


class ServiciosPersonalizados_View(viewsets.ModelViewSet):
    serializer_class = ServicioPersonalizados_serializers
    queryset = ServiciosPersonalizados.objects.all()





"""
#----------------------------------------------------------------
class ServiciosInternetListView(generics.ListAPIView):
    queryset = ServiciosInternet.objects.all()
    serializer_class = ServicioInternet_serializers

class ServiciosInternetDetailView(generics.RetrieveAPIView):
    queryset = ServiciosInternet.objects.all()
    serializer_class = ServicioInternet_serializers
#-----------------------------------------------------------------
class ServicioTelefonicoListView(generics.ListAPIView):
    queryset = ServicioTelefonico.objects.all()
    serializer_class = ServicioTelefonico_serializers

class ServicioTelefonicoDetailView(generics.RetrieveAPIView):
    queryset = ServicioTelefonico.objects.all()
    serializer_class = ServicioTelefonico_serializers
#-----------------------------------------------------------------
class ServiciosPersonalizadosListView(generics.ListAPIView):
    queryset = ServiciosPersonalizados.objects.all()
    serializer_class = ServicioPersonalizados_serializers

class ServiciosPersonalizadosDetailView(generics.RetrieveAPIView):
    queryset = ServiciosPersonalizados.objects.all()
    serializer_class =  ServicioPersonalizados_serializers
#-----------------------------------------------------------------

"""
