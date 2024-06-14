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
                    ContratosFucionador,
                    ZonaUsoMaterial,
                    Calendario,
                    AuditLog,
                    NombrePdfsSubidos,
                    ZonasAlmacen,
                    UsoProducto,
                    ProductosPrestados,
                    Devoluciones
                    )


class UsuarioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
        
        
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
    # nombre_producto_individual = serializers.CharField(source='id_producto_individual.nombre_producto_individual', read_only=True)
        
    
    
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

class ZonaUsoMaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = ZonaUsoMaterial
        fields = '__all__'



#-----------------------------------------------------------------------------
class ProductosImagenForm(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['imgProducto']
        

class CalendarioZerializers(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = '__all__'
        

class AuditLogZerializers(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        
        
        
class NombrePdfsSubidosZerializers(serializers.ModelSerializer):
    class Meta:
        model = NombrePdfsSubidos
        fields = '__all__'
        


class ZonasAlmacenZerializers(serializers.ModelSerializer):
    class Meta:
        model = ZonasAlmacen
        fields = '__all__'
        


class UsoProductoZerializers(serializers.ModelSerializer):

    usuario = UsuarioSerializers()

    class Meta:
        model = UsoProducto
        fields = ['id', 'cliente', 'tipoUsio', 'productos', 'fecha_uso', 'usuario']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['usuario'] = instance.usuario.nombre_completo  # Reemplaza 'nombre' con el campo real del nombre del usuario

        return representation



        

#----------------------------------------------------------
class ProductosPrestadosZerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductosPrestados
        fields='__all__'


#---------------------------------------------------------------------
class DevolucionesZerializers(serializers.ModelSerializer):
    class Meta:
        model=Devoluciones
        fields='__all__'
