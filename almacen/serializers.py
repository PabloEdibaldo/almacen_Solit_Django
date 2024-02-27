
from clientes.models import Clientes
from rest_framework import serializers
from .models import(
    # Categoria,
    Proveedor,
    Accesorio,
    Producto,
    Tecnico,
    Insta,
    ProductosInstalacion,
)
class Proveedor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'
class Accesorio_Serializer(serializers.ModelSerializer):
   
    class Meta:
        model = Accesorio
        fields = '__all__'
      
class Producto_Serializer(serializers.ModelSerializer):
    
   
    class Meta: 
        model = Producto
        fields = "__all__"
      
class Tecnico_Serializer(serializers.ModelSerializer):
   
    #Accesorio = serializers.StringRelatedField()
    class Meta: 
        model = Tecnico
        fields = '__all__'
      
class ProductosInstalacion_Serializers(serializers.ModelSerializer):
    producto = serializers.StringRelatedField()
    class Meta:
        model=ProductosInstalacion
        fields='__all__'
    
class Insta_Serializers(serializers.ModelSerializer):
    tecnico = serializers.StringRelatedField()
    cliente = serializers.StringRelatedField()
    #productos = serializers.StringRelatedField(many=True)
    class Meta:
        model = Insta
        fields = '__all__'