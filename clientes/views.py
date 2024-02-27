from rest_framework import viewsets

from .models import (
    Clientes,
    Facturacion,
    OtrosImpuestos,
    Notificacion,
    Instalacion
)
from .serializers import (
    Clientes_Serializer,
    Facturacion_Serializer,
    OtrosImpuestos_Serializer,
    Notificacion_Serializer,
    Instalacion_Serializer,
)

class Clientes_ViewSet(viewsets.ModelViewSet):
    serializer_class = Clientes_Serializer
    queryset = Clientes.objects.all()

class Facturacion_ViewSet(viewsets.ModelViewSet):
    serializer_class = Facturacion_Serializer
    queryset = Facturacion.objects.all()

class OtrosImpuestos_ViewSet(viewsets.ModelViewSet):
    serializer_class = OtrosImpuestos_Serializer
    queryset = OtrosImpuestos.objects.all()

class Notificacion_ViewSet(viewsets.ModelViewSet):
    serializer_class = Notificacion_Serializer
    queryset = Notificacion.objects.all()


class Instalcion_ViewSet(viewsets.ModelViewSet):
    serializer_class = Instalacion_Serializer
    queryset = Instalacion.objects.all()

