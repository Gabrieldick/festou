from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    bank = models.IntegerField( null=True, blank=True)
    account = models.CharField(max_length=15, null=True, blank=True)
    agency = models.CharField(max_length=15, null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    blocked = models.BooleanField(default=False)

class Place(models.Model):
    name = models.CharField(max_length=1024, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    location = models.CharField(max_length=1024, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    id_owner = models.IntegerField(null=True, blank=True)
    terms_of_use = models.CharField(max_length=8192, null=True, blank=True)
    STATE_CHOICES = [
        (-1, 'Rejected'),
        (0, 'Pending'),
        (1, 'Accepted'),
    ]
    checked = models.IntegerField(choices=STATE_CHOICES, default=0)

class Transaction(models.Model):
    id_client = models.IntegerField(null=True, blank=True)
    id_place = models.IntegerField(null=True, blank=True)
    id_advertiser = models.IntegerField(null=True, blank=True)
    initial_date = models.DateField(null=True, blank=True)
    payday  = models.DateField(null=True, blank=True)
    final_date = models.DateField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    payment = models.FloatField(null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_state = models.CharField(max_length=1024, null=True, blank=True) #Started, Canceled or Finished

class Score(models.Model):
    id_client = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    id_place = models.IntegerField(null=True, blank=True)
