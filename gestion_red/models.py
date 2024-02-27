from django.db import models
class Router(models.Model):
    nombre_router = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    usuario_api = models.CharField(max_length=100, null=True, blank=True)
    contrasenia_api = models.CharField(max_length=100, null=True, blank=True)
    tipo_router = models.CharField(max_length=100, null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    # Campos adicionales
    seguridad = models.CharField(max_length=100, null=True, blank=True)
    seguridad_alternativa = models.CharField(max_length=100, null=True, blank=True)
    configuracion_radius = models.CharField(max_length=100, null=True, blank=True)
    radius_nas_ip = models.CharField(max_length=80,null=True, blank=True)
    
    registro_trafico = models.CharField(max_length=100, null=True, blank=True)
    control_velocidad = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nombre_router
    
class RedesIpv4(models.Model):
    nombre = models.CharField(max_length=100)
    router = models.ForeignKey(Router, models.CASCADE,related_name="redes_ipv4",null=True)
    redip= models.CharField(max_length=100)
    cibr= models.CharField(max_length=100)
    uso_ipc = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    
#-------------------------------------------------------------------------------------------
class Monitoreo(models.Model):
    nombreEmisor = models.CharField(max_length=100)
    direccionIp= models.GenericIPAddressField()
    fabricante = models.CharField(max_length= 100)
    modelo = models.CharField(max_length=100,null=True,blank=True)
    usuario = models.CharField(max_length=100)
    contrasenia = models.CharField(max_length=100)
    monitireSNP = models.BooleanField()
    comunidadSNP = models.CharField(max_length=50)
    versionSNP = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreEmisor
    


class NapCaja(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    coordenadas = models.CharField(max_length=200,default=":")
    capacidad = models.IntegerField()
    fecha_instalacion = models.DateField(auto_now_add= True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    
class OltDevice(models.Model):
    name = models.CharField(max_length=100)
    olt_hardware_version = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    telnet_port = models.CharField(max_length=100)
    snmp_port = models.CharField(max_length=100)

    def __str__(self):
        return self.name
