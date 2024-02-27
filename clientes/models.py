from django.db import models

class Clientes(models.Model):
    numero_identificacion = models.CharField(max_length=20,null=True,blank=True)
    nombres_apellidos = models.CharField(max_length=200,null=True,blank=True)
    direccion = models.TextField(null=True,blank=True)
    telefono_casa = models.CharField(max_length=20,null=True,blank=True)
    telefono_movil = models.CharField(max_length=20,null=True,blank=True)
    correo = models.EmailField(null=True,blank=True)
    ubicacion = models.CharField(max_length=100,null=True,blank=True)
    observaciones = models.TextField(null=True,blank=True)
    name = models.CharField(max_length=50,null=True,blank=True)
    user = models.CharField(max_length=50,null=True,blank=True)
    def __str__(self):
        return self.nombres_apellidos
    
    
class Instalacion(models.Model):
    nombre = models.CharField(max_length=200,null=True,blank=True)
    direccion = models.TextField(null=True,blank=True)
    telefono_casa = models.CharField(max_length=20,null=True,blank=True)
    telefono_movil = models.CharField(max_length=20,null=True,blank=True)
    correo = models.EmailField(null=True,blank=True)
    ubicacion = models.CharField(max_length=100,null=True,blank=True)
    observaciones = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.nombre
    
    
class Facturacion(models.Model):
    tipo = models.CharField(max_length=50,null=True,blank=True)
    dia_pago = models.PositiveIntegerField(null=True,blank=True)
    crear_factura = models.CharField(max_length=50,null=True,blank=True)
    tipo_impuesto = models.CharField(max_length=50,null=True,blank=True)
    dias_gracia = models.CharField(max_length=50,null=True,blank=True)
    aplicar_corte = models.CharField(max_length=50,null=True,blank=True)
    fecha = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    mora = models.BooleanField(null=True,blank=True)
    reconexion = models.BooleanField(default=False)  # Campo para aplicar reconexión
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE,default=None, null=True,)  # Relación con Facturación

    def __str__(self):
        return self.tipo

class OtrosImpuestos(models.Model):
    inpuesto1 = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    inpuesto2 = models.DecimalField(max_digits=5, decimal_places=2, null = True)
    inpuesto3 = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    facturacion = models.ForeignKey(Facturacion, on_delete=models.CASCADE,default=None, null=True)

    def __str__(self):
        return "Otros Impuestos"

class Notificacion(models.Model):
    aviso_nueva_factura = models.BooleanField(default=False)
    aviso_en_pantalla = models.BooleanField(default=False)
    recordatorio_pago = models.BooleanField(default=False)
    recordatorio1 = models.BooleanField(default=False)
    recordatorio2 = models.BooleanField(default=False)
    recordatorio3 = models.BooleanField(default=False)

    def __str__(self):
        return "Notificaciones"

