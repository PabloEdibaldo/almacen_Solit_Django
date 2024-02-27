from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.db.models.signals import pre_save, pre_delete
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
import json

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
    
    nombre_completo=models.CharField(max_length=250)
    correo_electronico=models.CharField(max_length=250)
    numero_celular=models.CharField(max_length=15)
    equipo_trabajo=models.TextField()
    estatus=models.BooleanField(default=True)
    fecha_nacimiento=models.DateField()
    fotoPerfil = models.FileField(upload_to='fotosPerfiles/',null=True, blank=True)
    ubicacion=models.CharField(max_length=250)
    tipo_rol=models.CharField(max_length=250)
    password= models.CharField(max_length=50,default="NA")
    objects =UsuarioManager()


class Productos(models.Model):
    nombre_producto = models.CharField(max_length=250)
    marca = models.CharField(max_length=250, null=True, blank=True)
    modelo = models.CharField(max_length=250, null=True, blank=True)
    stock = models.IntegerField()
    observaciones = models.TextField(null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    unidad_medida = models.CharField(max_length=250, null=True, blank=True)
    empresa = models.CharField(max_length=250, null=True, blank=True)
    proveedor = models.CharField(max_length=250, null=True, blank=True)
    zona = models.CharField(max_length=250, null=True, blank=True)
    stock_minimo = models.IntegerField(null=True)

class ProductosIndividuales(models.Model):
    nombre_producto_individual = models.CharField(max_length=250)
    status = models.BooleanField()
    id_producto = models.ForeignKey('Productos', on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=250,null = True,blank = True)


class Reparto(models.Model):    
    fecha_solicitud = models.DateField(auto_now_add=True)
    nombre_administrador = models.CharField(max_length=250, null=True, blank=True)
    producto_cantidad = models.JSONField(null=True)
    nombre_solicitante = models.CharField(max_length=250,null=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    
   

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
    id_producto_individual = models.ForeignKey('ProductosIndividuales', on_delete=models.CASCADE, null=True, blank=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, null=True, blank=True)


class Historico(models.Model):
    # fecha_hora = models.DateTimeField(auto_now_add=True)
    # usuario = models.CharField(max_length=100, blank =True)
    # accion = models.CharField(max_length=50, null=True, blank =True)
    # tabla = models.CharField(max_length=50, null=True, blank =True)
    #class Historial(models.Model):
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
    
    
class ContratosFucionador(models.Model):
    fecha = models.DateField(auto_now_add=True,null=True, blank=True)
    productos = models.CharField(max_length=250,null=True, blank=True)
    status = models.CharField(max_length=250)
    nombre_usuario = models.CharField(max_length=100)
    
     
     
class Merma(models.Model):
    falla_descripcion = models.TextField()
    fecha_entrada = models.DateTimeField()
    status = models.SmallIntegerField()
    id_producto_individual = models.ForeignKey('ProductosIndividuales', on_delete=models.CASCADE)

class Pedido(models.Model):
    nombre = models.CharField(max_length=250)
    cantidad = models.IntegerField()

class Alerta(models.Model):
    nombre_producto = models.CharField(max_length=250)
    stock_actual = models.IntegerField()    
    

class PermisosProductosTecnico(models.Model):
    nombre = models.CharField(max_length=250)
    
  

class PermisosProductosFucionador(models.Model):
    nombre = models.CharField(max_length=250)
    



@receiver(pre_delete, sender=ProductosIndividuales)
def decrementar_stock(sender, instance, **kwargs):
     # Obtener los IDs de los productos individuales desde los argumentos
    ids_productos_individuales = kwargs.get('ids_productos_individuales', [])

    print(ids_productos_individuales, "ids")
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