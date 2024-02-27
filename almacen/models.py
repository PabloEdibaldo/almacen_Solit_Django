from django.db import models
from clientes.models import Clientes,Instalacion
from django.utils import timezone


class Proveedor(models.Model):
    Proveedor = models.CharField(max_length=100, null=True)
    Telefono = models.CharField(max_length=50)
    Gmail = models.CharField(max_length=50, null=True)
    Direccion = models.TextField(null=True)

    def __str__(self):
        return self.Proveedor


class Accesorio(models.Model):
    Nombre = models.CharField(max_length=50, null=True)
    Stock = models.IntegerField()
    Precio = models.IntegerField()
    ID_Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=20, default="valor_por_defecto",null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    ubicacion = models.CharField(max_length=300, default="valor_por_defecto",null=True, blank=True)
    Nombre = models.CharField(max_length=355, null=True, blank=True)
    descripcion = models.CharField(max_length=500, default="valor_por_defecto",null=True, blank=True) 
    marca = models.CharField(max_length=50, default="valor_por_defecto",null=True, blank=True)
    modelo = models.CharField(max_length=50, default="valor_por_defecto",null=True, blank=True)
    Stock = models.IntegerField(null=True, blank=True)
    observaciones = models.CharField(max_length=200,null=True, blank=True)
    image = models.TextField(verbose_name="Image Base64",null=True, blank=True)
    Precio = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    Proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE,null=True)
    area = models.CharField(max_length = 60, null = True, blank=True)
    observaciones = models.CharField(max_length=200,null=True, blank=True)
    def __str__(self):
        return self.Nombre

class Tecnico(models.Model):
    Nombre = models.CharField(max_length=100, null=True)
    Direccion = models.CharField(max_length=90, null=True)
    #Accesorio = models.ManyToManyField(Accesorio, related_name="Accesorios_del_tecnico")
    #fecha_Inicio = models.DateField()
    nivel_Educativo = models.CharField(max_length=100, default="NA")
    habilidates = models.CharField(max_length=100, default="NA")
    evaluacion = models.CharField(max_length=100,default=None)

    def __str__(self):
        return self.Nombre or "Tecnico"


class Insta(models.Model):
    observaciones = models.TextField(blank=True,null=True)
    tecnico = models.ForeignKey(Tecnico,on_delete=models.CASCADE,related_name="cliente")
    cliente = models.ForeignKey(Instalacion,on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto,related_name="Accesorios_del_tecnico")
    instalacion= models.DateTimeField()

    def __str__(self):
        return self.observaciones
    
    def get_productos(self):
        return self.productos.all()

class ProductosInstalacion(models.Model):
    instalacion = models.ForeignKey(Insta,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad_utilizada = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name
    
