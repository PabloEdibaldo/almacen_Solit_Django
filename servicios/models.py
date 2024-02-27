from django.db import models
#from gestion_red.models import Router

class  ServiciosInternet(models.Model):
    nombre_plan = models.CharField(max_length=100,)
    descripcion = models.TextField(blank = True,null = True)
    precio_plan = models.DecimalField(max_digits=10, decimal_places=2,blank = True,null = True)
    inpuesto = models.DecimalField(max_digits=5, decimal_places=2,blank = True,null = True)
    no_crear_reglas = models.BooleanField(default=False,blank = True,null = True)
    descarga_kbps = models.IntegerField(blank = True,null = True)
    subida_kbps = models.IntegerField(blank = True,null = True)
    limit_AT = models.IntegerField(blank = True,null = True)
    burst_limit = models.IntegerField(blank = True,null = True)
    burst_threshold = models.IntegerField(blank = True,null = True)
    burst_time = models.IntegerField(blank = True,null = True)
    prioridad = models.PositiveIntegerField(blank = True,null = True)
    addresslist = models.CharField(max_length=100,blank = True,null = True)
    prifile = models.CharField(max_length =100,blank = True,null = True)
    addresslistPCQ = models.CharField(max_length=100,blank = True,null = True)
    def __str__(self):
        return self.nombre_plan
    
class ServicioTelefonico(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    impuesto = models.DecimalField(max_digits=5, decimal_places=2)
    minutos = models.IntegerField()
    costo_tel_fijo = models.DecimalField(max_digits=6, decimal_places=2)
    costo_tel_movil = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.TextField()
    notas = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class ServiciosPersonalizados(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8,decimal_places=2)
    #nuevo_preco
    inpuestos = models.DecimalField(max_digits=8, decimal_places=2)
    Clave = models.CharField(max_length=50,blank=True)
    descripcion = models.CharField(max_length=50)

