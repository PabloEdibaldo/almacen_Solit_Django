from django.http import JsonResponse
import re
from rest_framework.response import Response
import fitz
from django.db.models import F
import tempfile
from rest_framework.parsers import MultiPartParser
from django.db import transaction
from rest_framework import viewsets
from .serializers import (UsuarioSerializers,
                          ProductosSerializers,
                          ProductosIndividualesSerializers,
                          MermaSerializers,
                          CarretesSerializers,
                          HistoricoSerializers,
                          MaterialInstalacionSerializers,
                          AlmacenSolitSerializers,
                          PedidoSolitSerializers,
                          AlertaSerializers,
                          RepartoSerializers,
                          PermisosProductosTecnicoSerializers,
                          PermisosProductosFucionadorSerializers,
                          ContratosFucionadorSerializers
                          ) 
from .models import  (Usuario,
                      Productos,
                      ProductosIndividuales,
                      Merma,
                      Carretes,
                      Historico,
                      MaterialInstalacion,
                      AlmacenSolit,
                      Pedido,
                      Alerta,
                      PermisosProductosTecnico,
                      PermisosProductosFucionador,
                      Reparto,
                      ContratosFucionador) 
# Create your views here

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from .models import decrementar_stock
from datetime import datetime




class ContratosFucionadorView(viewsets.ModelViewSet):
    serializer_class = ContratosFucionadorSerializers
    queryset = ContratosFucionador.objects.all()
    
    
    parser_classes = (MultiPartParser,)
    
    # def put(self, request, *args, **kwargs):
    #     print(request.data)  # Verifica si los datos del formulario se reciben correctamente
    #     archivo = request.FILES.get('archivo')
     
    #     return Response({"mensaje": "Archivo y datos actualizados correctamente"})

        


class UsuariosView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializers
    queryset = Usuario.objects.all()
    
    
class LoginView(ObtainAuthToken):
     def post(self, request):
        correo_electronico = request.data.get('correo_electronico')
        password = request.data.get('password')
        user = Usuario.objects.filter(correo_electronico=correo_electronico).first()
        
        if user is None:
            raise AuthenticationFailed('Usuario no encontrado!') 
       
        if not user.password ==password:
        
            raise AuthenticationFailed('Constraseña incorrecta!')

        refresh = RefreshToken.for_user(user)
        serializer = UsuarioSerializers(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        })
        
class ProductosView(viewsets.ModelViewSet):
    serializer_class = ProductosSerializers
    queryset = Productos.objects.all()
       
class MermaView(viewsets.ModelViewSet):
    serializer_class = MermaSerializers
    queryset = Merma.objects.all()
    
class CarretesView(viewsets.ModelViewSet):
    serializer_class = CarretesSerializers
    queryset = Carretes.objects.all()
    
class HistoricoView(viewsets.ModelViewSet):
    serializer_class = HistoricoSerializers
    queryset = Historico.objects.all()
    
class MaterialInstalacionView(viewsets.ModelViewSet):
    serializer_class = MaterialInstalacionSerializers
    queryset = MaterialInstalacion.objects.all()
   
    parser_classes = (MultiPartParser,)
    
    def post(self, request,     *args, **kwargs):
        print(request.data)  # Verifica si los datos del formulario se reciben correctamente
        archivo = request.FILES.get('archivo')
     
        return Response({"mensaje": "Archivo y datos actualizados correctamente"})

    
    
class AlmacenSolitView(viewsets.ModelViewSet):
    serializer_class = AlmacenSolitSerializers
    queryset = AlmacenSolit.objects.all()
  
class PedidoView(viewsets.ModelViewSet):
    serializer_class = PedidoSolitSerializers
    queryset = Pedido.objects.all()   

class AlertaView(viewsets.ModelViewSet):
    serializer_class = AlertaSerializers
    queryset = Alerta.objects.all()

class RepartoView(viewsets.ModelViewSet):
    serializer_class = RepartoSerializers
    queryset = Reparto.objects.all()  
    
    @action(detail=True, methods=['put'])
    def actualizar_nombre_administrador(self, request, pk=None):
        if request.method == 'PUT':
            reparto = self.get_object()
           
            nuevo_administrador = request.data.get('nombre_administrador', None)
           
            reparto.nombre_administrador = nuevo_administrador
            reparto.save()
                     
            productos_cantidad = reparto.producto_cantidad.get('productos', [])
           
            with transaction.atomic():  # Usar transacción para garantizar la integridad de los datos
                for producto in productos_cantidad:
                    nombre_producto = producto.get('nombre', None)
                    cantidad = producto.get('unidades', 0)
                   
                    # Realizar la búsqueda en ProductosIndividuales
                    ###############funciona###############
                    productos_individuales = ProductosIndividuales.objects.filter(
                        Q(nombre_producto_individual__iexact=nombre_producto)
                    )
                    
                      # Verificar si hay suficientes productos en stock
                    if productos_individuales.count() >= cantidad:
                        # Extraer la cantidad especificada de productos
                        productos_extraidos = productos_individuales[:cantidad]
                        
                  
                     # Puedes realizar acciones adicionales con los productos extraídos
                     # Obtener los IDs de los productos individuales
                        ids_productos_individuales = [producto_individual.id for producto_individual in productos_extraidos]
                        print(ids_productos_individuales)
                        decrementar_stock(instance=None,sender=None, ids_productos_individuales=ids_productos_individuales) 
                       
                       
                     
                        for producto_individual in productos_extraidos:
                            nueva_fecha = datetime.now()
                            codigo_barras = producto_individual.codigo_barras
                            
                            historic_existente = Historico.objects.filter(codigo_barras=codigo_barras).first()
                            
                            if historic_existente:
                                historic_existente.historial["historial"].append({
                                    "nombre_solicitante": reparto.nombre_solicitante,
                                    "fecha": nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
                                })
                                historic_existente.save()
                            else:
                                
                                nuevo_historico = Historico(
                                    codigo_barras = producto_individual.codigo_barras,
                                    nombre_producto = producto_individual.nombre_producto_individual,
                                
                                    historial={"histora":[
                                        {
                                        "nombre_solicitante":reparto.nombre_solicitante,
                                        "fecha":nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
                                        }
                                    ]}
                                    
                                )
                                nuevo_historico.save()
                    
                        print(f"Se extrajeron {cantidad} productos correctamente.")
                    else:
                    # Manejar la situación donde no hay suficientes productos en stock
                        print(f"No hay suficientes existencias para extraer {cantidad} productos de {nombre_producto}.")

        return Response({'mensaje': 'Nombre del administrador actualizado y productos verificados correctamente.'})


                   
   
    

     

class ProductosIndividualesView(viewsets.ModelViewSet):
    serializer_class = ProductosIndividualesSerializers
    def get_queryset(self):
        id_producto = self.request.query_params.get('id_producto')
        if id_producto:
            return ProductosIndividuales.objects.filter(id_producto=id_producto)
        else:
            return ProductosIndividuales.objects.all()
    
class PermisosProductosTecnicoView(viewsets.ModelViewSet):
    serializer_class = PermisosProductosTecnicoSerializers
    queryset = PermisosProductosTecnico.objects.all()   
    
    def create(self, request, *args, **kwargs):
        nombre = request.data.get('nombre', None)
        
        if nombre and PermisosProductosTecnico.objects.filter(nombre=nombre).exists():
            # El nombre ya existe
            return Response({"detail": "El nombre ya existe en la tbala de Productos tecnico."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().create(request, *args, **kwargs)
 
class PermisosProductosFucionadorView(viewsets.ModelViewSet):
     serializer_class = PermisosProductosFucionadorSerializers
     queryset = PermisosProductosFucionador.objects.all()   
     def create(self, request, *args, **kwargs):
        nombre = request.data.get('nombre', None)
        
        if nombre and PermisosProductosFucionador.objects.filter(nombre=nombre).exists():
             # El nombre ya existe
             return Response({"detail": "El nombre ya existe en la tabla de productos fucionador."}, status=status.HTTP_400_BAD_REQUEST)
        else:
             return super().create(request, *args, **kwargs)
    
@api_view(['POST'])
def upload_pdf(request):
    try:
        pdf_file = request.FILES['pdf_file']
        
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(pdf_file.read())
            temp_file_path = temp_file.name

        # Procesar el PDF
        text = extract_text_from_pdf(temp_file_path)
        
        matches_bobina = re.findall(r'(\d+)\s*BOBINA\n(.+?)\s*PARTIDA #', text, re.DOTALL)
        matches_kilometro = re.findall(r'(\d+)\s*KILOMET\n(.+?)\s*PARTIDA #', text, re.DOTALL)
        matches_pieza = re.findall(r'(\d+)\s*PIEZA\n(.+?)\s*PARTIDA #', text, re.DOTALL)
        matches =[]
        matches.append(matches_bobina)
        matches.append(matches_kilometro)
        matches.append(matches_pieza)
        
        
        # Aplicar la función limpiar_cadena a cada segundo elemento de las tuplas
        listas = [[[x[0], limpiar_cadena(x[1])] for x in sublista] for sublista in matches]

        
       
        tuplas_resultantes = []

        # Iterar sobre la lista y extraer elementos como tuplas
        for sublista in listas:
            for elemento in sublista:
                tuplas_resultantes.append(tuple(elemento))
        
        
        for tupla in tuplas_resultantes:
            canitadad = tupla[0]
            descripcion = tupla[1]
            
            Pedido.objects.create(nombre=descripcion,cantidad=int(canitadad))
        return Response({'success': 'PDF procesado correctamente'})
    except Exception as e:
        print(f"Error uploading or processing PDF: {e}")
        return Response({'error': 'Internal Server Error'}, status=500)
  
def limpiar_cadena(cadena):
    # Patrón para quitar todo hasta el segundo salto de línea (incluido)
    patron = re.compile(r'.*?\n.*?\n(.*)', re.DOTALL)
    # Aplicar el patrón y quedarse con la parte después del segundo salto de línea
    cadena_limpia = patron.sub(r'\1', cadena)
    
    
    return cadena_limpia

def extract_text_from_pdf(pdf_file):
    try:
        pdf_document = fitz.open(pdf_file)
        text = ""
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None



