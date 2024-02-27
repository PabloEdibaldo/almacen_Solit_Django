from rest_framework import serializers
from .models import(Productos,
                    Usuario,
                    Carretes,
                    Reparto, 
                   Historico,
                    Merma,
                    ProductosIndividuales,
                    MaterialInstalacion,
                    AlmacenSolit,
                    Pedido,
                    Alerta,
                    Reparto,
                    PermisosProductosTecnico,
                    PermisosProductosFucionador,
                    ContratosFucionador
                    )


class UsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        
        
class ProductosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'
        
class ProductosIndividualesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductosIndividuales
        fields = '__all__'
        
class RepartoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reparto
        fields = '__all__'
        

class MermaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Merma
        fields = '__all__'
        
class CarretesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carretes
        fields = '__all__'
        

class HistoricoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'
        
        
class MaterialInstalacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = MaterialInstalacion
        fields = '__all__'

class AlmacenSolitSerializers(serializers.ModelSerializer):
    class Meta:
        model = AlmacenSolit
        fields = '__all__'
        
   

class PedidoSolitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        
        
class RepartoSolitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reparto
        fields = '__all__'

class AlertaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = '__all__'
        
        
class PermisosProductosTecnicoSerializers(serializers.ModelSerializer):
    class Meta:
        model = PermisosProductosTecnico
        fields = '__all__'

class PermisosProductosFucionadorSerializers(serializers.ModelSerializer):
    class Meta:
        model = PermisosProductosFucionador
        fields = '__all__'

     
class ContratosFucionadorSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContratosFucionador
        fields = '__all__'

        
