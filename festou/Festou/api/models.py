from django.db import models

# Create your models here.
class User(models.Model):
    firstName = models.CharField(max_length=20, null=True, blank=True)
    lastName = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    bank = models.IntegerField( null=True, blank=True)
    account = models.CharField(max_length=15, null=True, blank=True)
    agency = models.CharField(max_length=15, null=True, blank=True)


class Place(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)