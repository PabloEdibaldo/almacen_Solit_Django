
import re
from rest_framework.response import Response
import fitz
from django.db.models import F
import tempfile
from rest_framework.parsers import MultiPartParser
from django.db import transaction
from rest_framework import viewsets
from django.contrib.auth import login, logout, authenticate
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
import json


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
                          ContratosFucionadorSerializers,
                          ZonaUsoMaterialSerializers,
                          CalendarioZerializers,
                          AuditLogZerializers,
                          NombrePdfsSubidosZerializers,
                          ZonasAlmacenZerializers,
                          UsoProductoZerializers,
                          ProductosPrestadosZerializers,
                          DevolucionesZerializers
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
# Create your views here

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from .models import decrementar_stock
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
import logging



class NombrePdfsSubidosView(viewsets.ModelViewSet):
    serializer_class = NombrePdfsSubidosZerializers
    queryset = NombrePdfsSubidos.objects.all()
   
logger = logging.getLogger('sistemaSolit')

class ContratosFucionadorView(viewsets.ModelViewSet):
    serializer_class = ContratosFucionadorSerializers
    queryset = ContratosFucionador.objects.all()
    
    
    logger.info('Obteniendo todos los productos')
    parser_classes = (MultiPartParser,)
    
class CalendarioView(viewsets.ModelViewSet):
    serializer_class = CalendarioZerializers
    queryset = Calendario.objects.all()
    
    permission_classes = [IsAuthenticated]



    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_destroy(self, instance):
        instance.modified_by = self.request.user
        instance.save()
        instance.delete()
        
class UsuariosView(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializers
    queryset = Usuario.objects.all()
    
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(modified_by=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(modified_by=self.request.user)

    # def perform_destroy(self, instance):
    #     instance.modified_by = self.request.user
    #     instance.save()
    #     instance.delete()
        
class LoginView(ObtainAuthToken):
     def post(self, request):
        correo_electronico = request.data.get('correo_electronico')
        password = request.data.get('password')
        user = Usuario.objects.filter(correo_electronico=correo_electronico).first()
        print(user)
        if user is None:
            raise AuthenticationFailed('Usuario no encontrado!') 
        
        if not user.check_password(password):
            raise AuthenticationFailed('Contraseña incorrecta!')

        refresh = RefreshToken.for_user(user)
        serializer = UsuarioSerializers(user)

        # Registrar la actividad de inicio de sesión
        AuditLog.objects.create(
            user=user,
            action='LOGIN',
            model_name='Usuario',
            object_id=user.id,
            changes='Inicio de sesión'
        )

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        })

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Registrar la actividad de cierre de sesión
            AuditLog.objects.create(
                user=request.user,
                action='LOGOUT',
                model_name='Usuario',
                object_id=request.user.id,
                changes='Cierre de sesión'
            )

            # Eliminar el token de actualización (opcional, dependiendo de cómo manejes los tokens)
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=204)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
                
class AuditLogView(viewsets.ModelViewSet):
    serializer_class = AuditLogZerializers
    queryset = AuditLog.objects.all()
    
    permission_classes = [IsAuthenticated]
    
class ProductosView(viewsets.ModelViewSet):
    serializer_class = ProductosSerializers
    queryset = Productos.objects.all()
    
    # permission_classes = [IsAuthenticated]
    
    # def perform_create(self, serializer):
    #     serializer.save(modified_by=self.request.user)

    # def perform_update(self, serializer):
    #     serializer.save(modified_by=self.request.user)

    # def perform_destroy(self, instance):
    #     instance.modified_by = self.request.user
    #     instance.save()
    #     instance.delete()
    @action(detail=True, methods=['put'])
    def editarProducto(self,request,pk=None):
        if request.method == 'PUT':
    
            stock = request.data.get("stock")
            id = request.data.get("id")

       
class MermaView(viewsets.ModelViewSet):
    serializer_class = MermaSerializers
    queryset = Merma.objects.all()
       
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
    
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_destroy(self, instance):
        instance.modified_by = self.request.user
        instance.save()
        instance.delete()
        
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_pedidos_by_pdf(request,pdf_id):
    
    
    try:
        
        pedidios = Pedido.objects.filter(pdf_subido=pdf_id)
        
        if not pedidios.exists():
            return Response({"error": "No se encontraron pedidos para el PDF especificado."}, status=404)
        serializer = PedidoSolitSerializers(pedidios, many=True)
        
        return Response(serializer.data)
    except NombrePdfsSubidos.DoesNotExist:
        return Response({"error":"Pdf no encontrado"},status=404)
    except Exception as e:
        return Response({'error': 'Internal Server Error'},status=500)
class AlertaView(viewsets.ModelViewSet):
    serializer_class = AlertaSerializers
    queryset = Alerta.objects.all()

class RepartoView(viewsets.ModelViewSet):
    serializer_class = RepartoSerializers
    queryset = Reparto.objects.all()  
    
    
    """
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_destroy(self, instance):
        instance.modified_by = self.request.user
        instance.save()
        instance.delete()

    """    
    def guradarProductosPorZonaDeUso(self, reparto, pk):
        try:
            # Obtener o crear el objeto ZonaUsoMaterial
            zona_uso_material, created = ZonaUsoMaterial.objects.get_or_create(pk=pk)

            # Obtener los productos del objeto Reparto
            nuevos_productos = reparto.producto_cantidad.get('productos', [])

            # Obtener los productos existentes del objeto ZonaUsoMaterial
            productos_existentes = zona_uso_material.productos or []

            for producto_nuevo in nuevos_productos:
                nombre_nuevo = producto_nuevo.get('nombre')
                unidades_nuevo = producto_nuevo.get('unidades')

                # Verificar si el producto ya existe en los productos existentes
                producto_existente = next((producto for producto in productos_existentes if producto.get('nombre') == nombre_nuevo), None)

                if producto_existente:
                    # Si el producto ya existe, aumentar la cantidad
                    producto_existente['unidades'] += unidades_nuevo
                else:
                    # Si el producto no existe, agregarlo a los productos existentes
                    productos_existentes.append({
                        'nombre': nombre_nuevo,
                        'unidades': unidades_nuevo
                    })

            # Guardar los productos actualizados en el objeto ZonaUsoMaterial
            zona_uso_material.productos = productos_existentes
            zona_uso_material.save()

            return Response({'mensaje': 'Productos guardados por zona de uso correctamente.'})

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

    def crearIstorialUsuario(self,productos,nombreCliente,tipoUsio,idSolicitante):
        print("Creado instorial usuario")
        usuario = Usuario.objects.get(id=idSolicitante)
        UsoProducto.objects.create(
             cliente= nombreCliente,
             tipoUsio=tipoUsio,
             productos= productos,
             usuario= usuario
             )

    def crearProductoPrestado(self, producto_id, nombreCliente):
        
        producto_details = Productos.objects.filter(id=producto_id)
        for detalle in producto_details:
            ProductosPrestados.objects.create(

                nombre_solicitante=nombreCliente,
                nombre_producto=detalle.nombre_producto,
                codigoInterno=detalle.codigoInterno,
                marca=detalle.marca,
                modelo=detalle.modelo,
                stock=1,
                observaciones=detalle.observaciones,
                unidad_medida=detalle.unidad_medida,
                empresa=detalle.empresa,
                proveedor=detalle.proveedor,
                zona=detalle.zona,
                stock_minimo=1,
                categoria=detalle.categoria,
                ZonaAlmacen=detalle.ZonaAlmacen)
                                 
        
            
    @action(detail=True, methods=['put'])
    def actualizar_nombre_administrador(self, request, pk=None):
        if request.method == 'PUT':
            reparto = self.get_object()
           
           
            nuevo_administrador = request.data.get('nombre_administrador', None)
            #Poner el producto en zonas 
            pk_zonaUso = request.data.get("id_zona",None)

            #Crear producto de inatalcion
            nombreCliente =request.data.get("nombreCliente",None)
            tipo_uso = request.data.get("TipoUsio", None)
            id_solicitante = request.data.get("idSolicitante", None)
            print(nombreCliente)
            print(id_solicitante)

            if nuevo_administrador:
                if pk_zonaUso:
                    self.guradarProductosPorZonaDeUso(reparto,pk_zonaUso)

              
                productos = reparto.producto_cantidad.get("productos",[])
                nombre_solicitante = request.data.get("nombre_solicitante",None)

                for producto in productos:
                    if producto.get("prestamo",False):
                        producto_id = producto["id_producto"]
                        self.crearProductoPrestado(producto_id,nombre_solicitante)



                self.crearIstorialUsuario(productos,nombreCliente,tipo_uso,id_solicitante)



            

            reparto.nombre_administrador = nuevo_administrador
            reparto.save()
                     
            productos_cantidad = reparto.producto_cantidad.get('productos', [])

            with transaction.atomic():  # Usar transacción para garantizar la integridad de los datos
                for producto in productos_cantidad:
                    nombre_producto = producto.get('nombre', None)
                    cantidad = producto.get('unidades', 0)
                   
                    # Realizar la búsqueda en ProductosIndividuales
                    ###############funciona###############
                    

                    productos_individuales = ProductosIndividuales.objects.filter(Q(nombre_producto_individual__iexact=nombre_producto))
                    
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
                                if 'historial' in historic_existente.historial:
                                    historic_existente.historial['historial'].append({
                                        "nombre_solicitante": reparto.nombre_solicitante,
                                        "fecha": nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
                                    })
                                else:
                                    # Si 'historial' no está presente, inicialízalo
                                    historic_existente.historial = {"historial": [{
                                        "nombre_solicitante": reparto.nombre_solicitante,
                                        "fecha": nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
                                    }]}
                                historic_existente.save()
                            else:
                                # Crear un nuevo objeto Historico con 'historial' inicializado
                                nuevo_historico = Historico(
                                    codigo_barras=producto_individual.codigo_barras,
                                    nombre_producto=producto_individual.nombre_producto_individual,
                                    historial={"historial": [{
                                        "nombre_solicitante": reparto.nombre_solicitante,
                                        "fecha": nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")
                                    }]}
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
        
class CarretesView(viewsets.ModelViewSet):
    

    serializer_class = CarretesSerializers
    queryset = Carretes.objects.select_related('id_producto')
    
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
@permission_classes([IsAuthenticated])
def upload_pdf(request):
    try:
        
        pdf_file = request.FILES['pdf_file']     
        user = request.user
        if NombrePdfsSubidos.objects.filter(nombrePdf = pdf_file).exists():
            return Response({'error': 'El PDF ya fue subido anteriormente'}, status=400)
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(pdf_file.read())
            temp_file_path = temp_file.name

        # Procesar el PDF
        text = extract_text_from_pdf(temp_file_path)
        
        matches_bobina = re.findall(r'(\d+)\s*BOBINA\n(.+?)\s*PARTIDA #', text, re.DOTALL)
        matches_kilometro = re.findall(r'(\d+)\s*KILOMET\n(.+?)\s*PARTIDA #', text, re.DOTALL)
        matches_pieza = re.findall(r'(\d+)\s*PIEZA\n(.+?)\s*PARTIDA #', text, re.DOTALL)

# Para cada tupla encontrada, añadimos el tipo de artículo correspondiente
        matches_bobina = [list(match) + ["bobina"] for match in matches_bobina]
        matches_kilometro = [list(match) + ["kilometro"] for match in matches_kilometro]
        matches_pieza = [list(match) + ["pieza"] for match in matches_pieza]

        matches = []
        matches.append(matches_bobina)
        matches.append(matches_kilometro)
        matches.append(matches_pieza)
        
        pdf_subido = NombrePdfsSubidos.objects.create(
            nombrePdf =pdf_file, 
            fecha_solicitud= datetime.now(),
            user = user,
            nameUser= user.nombre_completo)
    
# Extraer la parte central de cada cadena en las tuplas y crear objetos Pedido
        for match_list in matches:
            for match in match_list:
                cantidad = match[0]
                descripcion = match[1].split('\n')  # Extraer la parte central
                
                modelo = match[1].split('\n')[1]  # Asignar la parte central a modelo
                tipo = match[2]  # Obtener el tipo de artículo
                
                Pedido.objects.create(nombre=descripcion[2],
                                      cantidad=int(cantidad),
                                      modelo=modelo,
                                      unidad=tipo,
                                      pdf_subido=pdf_subido)

        return Response({'success': 'PDF procesado correctamente'})
    except Exception as e:
        print(f"Error uploading or processing PDF: {e}")
        return Response({'error': 'Internal Server Error'}, status=500)

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def devolucionProducto(request):
    id_producto = request.data.get("id_producto")
    cantidad = int(request.data.get("cantidad"))

    try:
        producto = Productos.objects.get(id= id_producto)
    except Productos.DoesNotExist:
        return Response({"Error":"Producto no encontrado."},status=404)

    producto.stock += cantidad
    producto.save()

    Devoluciones.objects.create(
        nombreSolicitante=request.data.get("nombreSolicitante"),
        producto=producto,
        cantidad=cantidad)

    return Response({"success":"Producto actualizado y devolucion registrada con exito prro"},status=200)

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

class AgregarImagenProducto(APIView):
    def post(self, request, producto_id):
        try:
            producto = Productos.objects.get(id=producto_id)
            imagen = request.FILES.get('img')
            print(imagen)
            if imagen:
                producto.imgProducto = imagen
                producto.save()
                serializer = ProductosSerializers(producto)
                return Response(serializer.data, status=200)
            else:
                return Response({'error': 'No se proporcionó ninguna imagen'}, status=400)
        except Productos.DoesNotExist:
            return Response({'error': 'El producto no existe'}, status=404)

class ZonasusoMaterialView(viewsets.ModelViewSet):
    serializer_class = ZonaUsoMaterialSerializers
    queryset = ZonaUsoMaterial.objects.all()
    
    
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_destroy(self, instance):
        instance.modified_by = self.request.user
        instance.save()
        instance.delete()
    
class ZonasAlmacenView(viewsets.ModelViewSet):
    serializer_class = ZonasAlmacenZerializers
    queryset = ZonasAlmacen.objects.all()
    
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def perform_destroy(self, instance):
        instance.modified_by = self.request.user
        instance.save()
        instance.delete()
    
class UsoProductoView(viewsets.ModelViewSet):
    serializer_class = UsoProductoZerializers
    queryset = UsoProducto.objects.all()

class ProductosPrestadosView(viewsets.ModelViewSet):
    serializer_class = ProductosPrestadosZerializers
    queryset = ProductosPrestados.objects.all()

class DevolucionesView(viewsets.ModelViewSet):
    serializer_class = DevolucionesZerializers
    queryset = Devoluciones.objects.all()

@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def crearProductosPorCodigoDeBarras(request):
    id_producto = request.data.get("id_producto")
    codigos_barras = request.data.get("codigosBarras")
    print("codigos",codigos_barras)

    try:
        producto = Productos.objects.get(id=id_producto)
    except Productos.DoesNotExist:
        return Response({"Error": "Producto no encontrado."}, status=404)

    longitud = len(codigos_barras)

    # print("lonf",longitud)
    # Aumentar el stock del producto con la cantidad de códigos de barras
    # producto.stock += longitud
    # producto.save()

    # Filtrar productos individuales que no tengan código de barras asignado
    productos_individuales = ProductosIndividuales.objects.filter(id_producto=producto.id, codigo_barras__isnull=True)

    if productos_individuales.count() < longitud:
        return Response({"Error": "No hay suficientes productos individuales disponibles."}, status=400)

    # Asignar los códigos de barras a los productos individuales
    for i, producto_individual in enumerate(productos_individuales[:longitud]):
        producto_individual.codigo_barras = codigos_barras[i]
        producto_individual.save()

    return Response({"success": "Productos individuales actualizados correctamente."}, status=200)

@api_view(['POST'])
def sacarMaterialPorCodigoBarras(request):

    codigos = request.data.get("codigos")
    idReparto = request.data.get('id_reparto')
    nuevo_administrador = request.data.get('nombre_administrador')

    bandera = False

    try:
        reparto = Reparto.objects.get(id= idReparto)
    except Reparto.DoesNotExist:
        return Response({"Error":"Reparto no encontrado"},status = 404)


    reparto.nombre_administrador = nuevo_administrador
    reparto.save()

    productos_reparto = reparto.producto_cantidad.get('productos', [])
    print(productos_reparto)

    for producto in productos_reparto:
        id_producto = producto.get("id_producto")
        print(id_producto)

        if id_producto:
            try:
                producto_restar = Productos.objects.get(id=id_producto)
            except Productos.DoesNotExist:
                return Response({"Error": f"Producto con id {id_producto} no encontrado."}, status=404)

            producto_restar.stock -= producto.get("unidades", 0)
            producto_restar.save()

            productos_individuales = ProductosIndividuales.objects.filter(id_producto=id_producto, codigo_barras__in=codigos)
            for producto_individual in productos_individuales:
                producto_individual.delete()
                bandera = True


    print(reparto.nombre_administrador)

    if reparto.nombre_administrador:
        if reparto.id_zona:
            RepartoView.guradarProductosPorZonaDeUso(reparto, reparto.id_zona)

        nombre_solicitante = reparto.nombre_solicitante
        

        for producto in productos_reparto:
            if producto.get("prestamo", False):
                producto_id = producto["id_producto"]
               
                RepartoView().crearProductoPrestado(producto_id,nombre_solicitante)
                
        
        if bandera:
            RepartoView().crearIstorialUsuario(
                productos_reparto,
                reparto.nombre_solicitante,
                reparto.TipoUsio,
                reparto.idSolicitante)

        return Response({"success": "Material procesado correctamente."}, status=200)


    # try:
    #     reparto = Reparto.objects.get(id= idReparto)
    # except Reparto.DoesNotExist:
    #     return Response({"Error":"Reparto no encontrado"},status = 404)


    # reparto.nombre_administrador = nuevo_administrador
    # reparto.save()

    # productos_reparto = reparto.producto_cantidad.get('productos', [])

    # #Obtener los los ids de los productos 
    # for producto in productos_reparto:
    #     id_producto = producto.get("id_producto")
    #     #buscar los productos con el id y editar sus stocks
    #     producto_restar = Productos.objects.get(id=id_producto)

    #     producto_restar.stock -= producto.get("unidades")
    #     producto_restar.save()

    #     if id_producto:

    #         productos_individuales = ProductosIndividuales.objects.filter(id_producto=id_producto, codigo_barras__in=codigos)
    #         for producto_individual in productos_individuales:
    #             producto_individual.delete()

    # if reparto.nombre_administrador:
    #     if reparto.id_zona:
    #         RepartoView.guradarProductosPorZonaDeUso(reparto,reparto.id_zona)

            
    #         nombre_solicitante = reparto.nombre_solicitante


    #         for producto in productos_reparto:
    #                 if producto.get("prestamo",False):
    #                     producto_id = producto["id_producto"]
    #                     RepartoView.crearProductoPrestado(producto_id,nombre_solicitante)



    #         RepartoView.crearIstorialUsuario(
    #             productos_reparto,
    #             reparto.nombre_solicitante,
    #             reparto.tipo_uso,
    #             reparto.id_solicitante)

