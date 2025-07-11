from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    User=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ("XS", "XS"), ("S", "S"), ("M", "M"), 
        ("L", "L"), ("XL", "XL"), ("XXL", "XXL"),
        ("7-8Y", "7-8Y"), ("8-9Y", "8-9Y"), 
        ("10-11Y", "10-11Y"), ("12-13Y", "12-13Y"), 
        ("14-15Y", "14-15Y")
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.size} ({self.stock} left)"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"{self.product.name} Image"
