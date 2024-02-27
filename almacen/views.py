
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import (
    Proveedor,
    Accesorio,
    Producto,
    Tecnico,
    Insta,
    ProductosInstalacion
)

from .serializers import (
    Proveedor_Serializer,
    Accesorio_Serializer,
    Producto_Serializer,
    Tecnico_Serializer,
    Insta_Serializers,
    ProductosInstalacion_Serializers
)
import json
class Proveedor_view(viewsets.ModelViewSet):
    serializer_class = Proveedor_Serializer
    queryset = Proveedor.objects.all()

class Accesorio_view(viewsets.ModelViewSet):
    serializer_class = Accesorio_Serializer
    queryset = Accesorio.objects.all()

class Producto_view(viewsets.ModelViewSet):
    serializer_class = Producto_Serializer
    queryset = Producto.objects.all()

class Tecnico_view(viewsets.ModelViewSet):
    serializer_class = Tecnico_Serializer
    queryset = Tecnico.objects.all()
    
   
        
class Insta_view(viewsets.ModelViewSet):
    serializer_class = Insta_Serializers
    queryset = Insta.objects.all()
    
    def create(self, serializer):
        tecnico = serializer.save()
        accesorios_ids = self.request.data.get('Accesorio', [])  # Obtener la lista de IDs de accesorios del request

        for accesorio_id in accesorios_ids:
            accesorio = Accesorio.objects.get(id=accesorio_id)
            tecnico.Accesorio.add(accesorio)  # Asignar accesorio al técnico
            accesorio.Stock -= 1  # Disminuir el stock del accesorio en 1
            accesorio.save()  # Guardar el accesorio actualizado

        return Response(serializer.data)
    
    
class ProductosInstalacion_view(viewsets.ModelViewSet):
    serializer_class = ProductosInstalacion_Serializers
    queryset = ProductosInstalacion.objects.all()
class InstalacionViewSet(viewsets.ViewSet):
    serializer_class = Insta_Serializers  # Definir el serializador aquí
    
    def create(self, request):
        if request.method == 'POST':
            data = request.data  # No es necesario json.loads
          
            observaciones = data.get('observaciones')
            tecnico_id = data.get('tecnico')
            cliente_id = data.get('cliente')
            productos = data.get('productos',[])
            instalacion = data.get('instalacion')

            # Crear una nueva instancia de Insta
            nueva_instalacion = Insta.objects.create(
                observaciones=observaciones,
                tecnico_id=tecnico_id,
                cliente_id=cliente_id,
                instalacion=instalacion,
            )

            # Guardar los productos en la tabla ProductoEnInstalacion
            for producto_data in productos:
                if isinstance(producto_data, dict): 
                    producto_id = producto_data.get('id')
                    cantidad = producto_data.get('cantidad_utilizada')
                    
                    
                    ProductosInstalacion.objects.create(
                        instalacion=nueva_instalacion,
                        producto_id=producto_id,
                        cantidad_utilizada=cantidad,
                    )
                    producto = Producto.objects.get(pk=producto_id)
                    producto.Stock -= cantidad
                    producto.save()
                
            else:
                    # Manejar el caso en que producto_data no sea un diccionario
                    print(f"Error: producto_data no es un diccionario. Valor actual: {producto_data}")

            return Response({'message': 'Instalación guardada exitosamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
    def delete(self, request, pk):
        instalacion_id = pk

        instalacion = Insta.objects.get(id=instalacion_id)
        instalacion.delete()
        
        productos_instalacion = ProductosInstalacion.objects.filter(instalacion=instalacion)
        productos_instalacion.delete()

        return Response({'message': 'Instalación eliminada exitosamente'}, status=status.HTTP_200_OK)
    def update(self, request, pk):
        instalacion_id = pk
        data = request.data

        observaciones = data.get('observaciones')
        tecnico_id = data.get('tecnico')
        cliente_id = data.get('cliente')
        nueva_instalacion_fecha = data.get('instalacion')  # Cambiado el nombre de la variable

        instalacion = Insta.objects.get(id=instalacion_id)
        instalacion.observaciones = observaciones
        instalacion.tecnico_id = tecnico_id
        instalacion.cliente_id = cliente_id
        instalacion.instalacion = nueva_instalacion_fecha  # Usar el nuevo nombre de la variable
        instalacion.save()

        # Actualizar los productos asociados
        productos_instalacion_actualizados = data.get('productos', [])
        for producto_data in productos_instalacion_actualizados:
            if isinstance(producto_data, dict): 
                producto_id = producto_data.get('id')
                cantidad = producto_data.get('cantidad_utilizada')
                ProductosInstalacion.objects.filter(instalacion=instalacion, producto_id=producto_id).update(cantidad_utilizada=cantidad)

        return Response({'message': 'Instalación actualizada exitosamente'}, status=status.HTTP_200_OK)
