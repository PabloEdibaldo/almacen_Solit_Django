from rest_framework import serializers
#from api.serializers import UserPublicSerializer
from .models import (
    ServiciosInternet,
    ServiciosPersonalizados,
    ServicioTelefonico
)

class ServicioInternet_serializers(serializers.ModelSerializer):
 #   author = UserPublicSerializer(source='user', read_only=True)
    class Meta:
        model = ServiciosInternet
        fields = '__all__'

class ServicioPersonalizados_serializers(serializers.ModelSerializer):
  #  author = UserPublicSerializer(source='user', read_only=True)
    class Meta:
        model = ServiciosPersonalizados
        fields = '__all__'

class ServicioTelefonico_serializers(serializers.ModelSerializer):
   # author = UserPublicSerializer(source='user', read_only=True)
    class Meta:
        model=ServicioTelefonico
        fields = '__all__'
        

