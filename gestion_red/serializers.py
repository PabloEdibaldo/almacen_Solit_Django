from rest_framework import serializers

from . models import (Router,
                    RedesIpv4,
                    Monitoreo,
                    NapCaja,
                    OltDevice)

class Router_serializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = '__all__'

class Redes_ipb4_serializers(serializers.ModelSerializer):
    class Meta:
        model = RedesIpv4
        fields = '__all__'

class Monitoreo_serializer(serializers.ModelSerializer):
    class Meta:
        model=Monitoreo
        fields = '__all__'

class NapCaja_serializer(serializers.ModelSerializer):
    class Meta:
        model=NapCaja
        fields = '__all__'
        

class OltDevice_serializer(serializers.ModelSerializer):
    class Meta:
        model=OltDevice
        fields = '__all__'