from rest_framework import serializers
from .models import (
    Clientes,
    Facturacion,
    OtrosImpuestos,
    Notificacion,
    Instalacion
)



class Clientes_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Clientes
        fields = '__all__'
        
class Facturacion_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Facturacion
        fields = '__all__'
        
class OtrosImpuestos_Serializer(serializers.ModelSerializer):
    class Meta:
        model = OtrosImpuestos
        fields = '__all__'

class Notificacion_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
        
class Instalacion_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Instalacion
        fields = '__all__'
        
    