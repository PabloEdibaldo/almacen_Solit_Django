from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
import uuid

class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(correo_electronico)
        user = self.model(correo_electronico=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(correo_electronico, password, **extra_fields)

class Usuario(AbstractBaseUser):
    USERNAME_FIELD = "correo_electronico"
    
    nombre_completo=models.CharField(max_length=250 )
    correo_electronico=models.CharField(max_length=250,unique=True)
    numero_celular=models.CharField(max_length=15)
    equipo_trabajo=models.TextField(null=True, blank=True)
    estatus=models.BooleanField(default=True)
    fecha_nacimiento=models.DateField()
    fotoPerfil = models.FileField(upload_to='fotosPerfiles/',null=True, blank=True)
    ubicacion=models.CharField(max_length=250)
    tipo_rol=models.CharField(max_length=250)
    password= models.CharField(max_length=128)
    objects =UsuarioManager()

class ZonasAlmacen(models.Model):
    NombreZona = models.CharField(max_length=250)
    
    def __str__(self):
        return f"{self.NombreZona}"

class Productos(models.Model):
    nombre_producto = models.CharField(max_length=250, null=True,blank=True)
    codigoInterno = models.CharField(max_length=10,null=True,)
    marca = models.CharField(max_length=250, null=True, blank=True)
    modelo = models.CharField(max_length=250, null=True, blank=True)
    stock = models.IntegerField()
    observaciones = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    unidad_medida = models.CharField(max_length=250, null=True, blank=True)
    empresa = models.CharField(max_length=250, null=True, blank=True)
    proveedor = models.CharField(max_length=250, null=True, blank=True)
    
    
    zona = models.CharField(max_length=250, null=True, blank=True)
    
    stock_minimo = models.IntegerField(null=True)
    imgProducto = models.FileField(upload_to='imgProducto/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])], null=True, blank=True)
    categoria = models.CharField(max_length=250, null=True)
    fecha_actualizacion = models.DateField(null=True)
    automatico_insert = models.BooleanField(default=False)
    modified_by = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    ZonaAlmacen = models.ForeignKey(ZonasAlmacen, on_delete=models.SET_NULL, null=True, blank=True)
    
    productoParaPrestar = models.BooleanField(default=False,null=True, blank=True)
    
    
class ProductosPrestados(models.Model):

    nombre_solicitante = models.CharField(max_length=250,null = True,blank = True)
    #-----------------------------------------------------------------------------
    nombre_producto = models.CharField(max_length=250, null=True,blank=True)
    codigoInterno = models.CharField(max_length=10,null=True,)
    marca = models.CharField(max_length=250, null=True, blank=True)
    modelo = models.CharField(max_length=250, null=True, blank=True)
    stock = models.IntegerField()
    observaciones = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    unidad_medida = models.CharField(max_length=250, null=True, blank=True)
    empresa = models.CharField(max_length=250, null=True, blank=True)
    proveedor = models.CharField(max_length=250, null=True, blank=True)
    zona = models.CharField(max_length=250, null=True, blank=True)
    
    stock_minimo = models.IntegerField(null=True)
    categoria = models.CharField(max_length=250, null=True)
    fecha_actualizacion = models.DateField(null=True)
    automatico_insert = models.BooleanField(default=False)
    modified_by = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    ZonaAlmacen = models.CharField( max_length=50, null=True, blank=True)














class ProductosIndividuales(models.Model):
    nombre_producto_individual = models.CharField(max_length=250)
    status = models.BooleanField()
    id_producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=250,null = True,blank = True)
    estado = models.CharField(max_length=200, null=True)

class Reparto(models.Model):    
    fecha_solicitud = models.DateField(auto_now_add=True)
    nombre_administrador = models.CharField(max_length=250, null=True, blank=True)
    producto_cantidad = models.JSONField(null=True)
    nombre_solicitante = models.CharField(max_length=250,null=True)
    #id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    id_zona = models.ForeignKey('ZonaUsoMaterial', on_delete=models.CASCADE, null=True)
    nombreCliente = models.CharField(max_length=250, null=True, blank=True)
    idSolicitante = models.IntegerField(null=True,blank=True)
    modified_by = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    TipoUsio= models.CharField(max_length=250, null=True, blank=True)

   
class AlmacenSolit(models.Model):
    
    fecha_hora_entrada = models.DateTimeField()
    cantidad_entrada = models.IntegerField()
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    cantidad_salida = models.IntegerField(null=True, blank=True)
    id_producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)

class Carretes(models.Model):

    metraje_inicial = models.IntegerField()
    metraje_usado = models.IntegerField(null=True, blank=True)
    id_producto = models.ForeignKey('Productos', on_delete=models.CASCADE, null=True, blank=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)
    luegarDeUso = models.CharField(max_length=250, null=True, blank=True)
    descripcion = models.CharField(max_length=250, null=True, blank=True)

class Historico(models.Model):
    
    codigo_barras = models.CharField(max_length=250,null=True,blank =True)
    nombre_producto = models.CharField(max_length=250,null=True,blank =True)
    historial = models.JSONField(null=True,blank =True)
    nombre_solicitante = models.CharField(max_length=250, null=True,blank =True)
    uso = models.CharField(max_length=250,null=True,blank =True)    

class MaterialInstalacion(models.Model):
    fecha_instalacion = models.DateField(auto_now_add=True)
    telefono_cliente = models.CharField(max_length=13)
    nombre_cliente = models.CharField(max_length=250)
    tipo_servicio = models.CharField(max_length=250)
    nombre_instalador = models.CharField(max_length=250,null=True, blank=True)
    direccion_cliente = models.CharField(max_length=250, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    prefirma_trabajador = models.JSONField(null=True,)
    prefirma_cliente = models.JSONField(null=True,)
    informacionFibra = models.JSONField(null=True)
    informacionAntena = models.JSONField(null=True)
    archivoTerminal = models.FileField(upload_to='evidencias/terminal/',null=True, blank=True)
    archivoRouter = models.FileField(upload_to='evidencias/router/',null=True, blank=True)
    archivoPTerminal = models.FileField(upload_to='evidencias/pterminal/',null=True, blank=True)
    archivoPosicionAntena = models.FileField(upload_to='evidencias/posicionAntena/',null=True, blank=True)
    archivoInformacionAntena = models.FileField(upload_to='evidencias/informacionAntena/',null=True, blank=True)
    archivoNavegacion = models.FileField(upload_to='evidencias/navegacion/',null=True, blank=True)
    
class ZonaUsoMaterial(models.Model):
    zona = models.CharField(max_length=250,null=True, blank=True)
    fraccionamiento = models.CharField(max_length=250,null=True, blank=True)
    colona = models.CharField(max_length=250,null=True, blank=True)
    juntaAuxiliar = models.CharField(max_length=250,null=True, blank=True)
    productos =models.JSONField(null= True)
        
class ContratosFucionador(models.Model):
    fecha = models.DateField(auto_now_add=True,null=True, blank=True)
    productos = models.CharField(max_length=250,null=True, blank=True)
    status = models.CharField(max_length=250)
    nombre_usuario = models.CharField(max_length=100)
    
class Merma(models.Model):
    falla_descripcion = models.TextField()
    fecha_entrada = models.DateField(auto_now_add=True)
    status = models.SmallIntegerField()
    id_producto_individual = models.ForeignKey('ProductosIndividuales', on_delete=models.CASCADE)

class NombrePdfsSubidos(models.Model):
    nombrePdf = models.CharField(max_length=255)
    fecha_solicitud = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nameUser = models.CharField(max_length=50,null=True,blank=True)

class Pedido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    modelo = models.CharField(null=True,max_length=250)
    unidad = models.CharField(null=True,max_length=250)
    fecha = models.DateField(auto_now_add=True,null=True, blank=True)
    modified_by = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    pdf_subido = models.ForeignKey(NombrePdfsSubidos, on_delete=models.CASCADE, related_name='pedidos',null=True, blank=True)

class Alerta(models.Model):
    nombre_producto = models.CharField(max_length=250)
    stock_actual = models.IntegerField()    
    
class Calendario(models.Model):
    title = models.CharField(max_length=600)
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    modified_by = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
class PermisosProductosTecnico(models.Model):
    nombre = models.CharField(max_length=250)
    
class PermisosProductosFucionador(models.Model):
    nombre = models.CharField(max_length=250)

class Devoluciones(models.Model):
    nombreSolicitante = models.CharField(max_length=200)
    producto = models.JSONField(null= True)
    fecha_uso = models.DateTimeField(auto_now_add=True)
    cantidad = models.IntegerField()

    


class UsoProducto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=250,null=True, blank=True)
    tipoUsio = models.CharField(max_length=250,null=True, blank=True)
    productos = models.JSONField(null= True, blank=True)
    fecha_uso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.producto} - {self.cantidad} - {self.fecha_uso}"

    
    
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
    ]

    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action} - {self.model_name} - {self.object_id}"



@receiver(pre_delete, sender=ProductosIndividuales)
def decrementar_stock(sender, instance, **kwargs):
     # Obtener los IDs de los productos individuales desde los argumentos
    ids_productos_individuales = kwargs.get('ids_productos_individuales', [])

   
    for id_producto_individual in ids_productos_individuales:
        try:
            # Obtener el objeto ProductosIndividuales
            
            producto_individual = ProductosIndividuales.objects.get(id=id_producto_individual)

            # Decrementar el stock en Productos
            producto = producto_individual.id_producto
            producto.stock -= 1
            producto.save()
            
            # Eliminar el objeto ProductosIndividuales
            producto_individual.delete()

        except Productos.DoesNotExist:
            pass



