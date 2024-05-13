from django.db import models
from django.contrib.auth.models import User 


class Products(models.Model):
    Product_Name = models.CharField(max_length=255)
    Product_Price = models.FloatField()
    Product_Discription = models.CharField(max_length=1000)
    Product_Stock = models.IntegerField()
    Stock_trush = models.IntegerField()
    Product_Image = models.FileField(upload_to="product_image")
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    options = (("Mens","Mens"),("Womans","Womans"),("Kids","Kids"))
    Product_Category = models.CharField(max_length=20,choices=options, default="Mens")
    options1 = (("Shirts","Shirts"),("Jeans","Jeans"),("SwimWear","SwimWear"),("Shoes","Shoes"))

    Product_Category_sub = models.CharField(max_length=20,choices=options1,default="Shirts")


class Cart(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    items = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Checkout(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    items = models.IntegerField()
    total_price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pytment_status = models.BooleanField(default=True)
    delivery_status = models.CharField(max_length=20)








