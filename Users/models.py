from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=15)
    image= models.ImageField(upload_to='static/images/',null=True, default="static/images/default-image.png")

class Product(models.Model):
    CATEGORIES = (
        ('Fruit','Fruit'),
        ('Vegetable','Vegetable')
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=10000)
    image= models.ImageField(upload_to='static/images/')
    description = models.TextField()
    categories = models.CharField(max_length=100,choices=CATEGORIES)

class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=True)
    quantity = models.IntegerField(default=0)
    cost = models.DecimalField(decimal_places=2,max_digits=10000,default=0)
    status = models.BooleanField(default=False)