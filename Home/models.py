from django.db import models
from django.contrib.auth.models import User


class BillingAdress(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=11)
    address =  models.CharField(max_length=255)
    city = models.CharField(max_length=11)
    state = models.CharField(max_length=11)
    zipcode = models.CharField(max_length=11)
    country = models.CharField(max_length=11)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)




