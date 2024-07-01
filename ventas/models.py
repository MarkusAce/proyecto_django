from django.db import models
from django.contrib.auth.models import User
import os
import hashlib


def get_image_path(instance, filename):
    return os.path.join('pagina', filename)

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Consola(models.Model):
    id_consola = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Videojuego(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_juego = models.CharField(max_length=100)
    stock_juego = models.IntegerField()
    descripcion = models.TextField()
    image = models.ImageField(upload_to=get_image_path)
    precio = models.IntegerField()
    id_consola = models.ForeignKey(Consola, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_juego




class Usuario(models.Model):
    rut = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=100)
    a_paterno = models.CharField(max_length=100)
    a_materno = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    email1 = models.EmailField()
    cel1 = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.rut} - {self.nombre} {self.a_paterno} {self.a_materno}"
    
    def set_password(self, raw_password):
        self.password = hashlib.sha256(raw_password.encode()).hexdigest()
    
class Vendedor(models.Model):
    rut = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=100)
    a_paterno = models.CharField(max_length=100)
    a_materno = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    email1 = models.EmailField()
    cel1 = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    rut = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    stock = models.IntegerField()
    direccion_envio = models.TextField()

    def __str__(self):
        return f"Compra #{self.id_compra} - Usuario: {self.rut}, Producto: {self.id_producto}"
    
class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

class ElementoCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    videojuego = models.ForeignKey(Videojuego, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.IntegerField()




