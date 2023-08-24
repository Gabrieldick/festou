from rest_framework.response import Response
from .models import Place, Transaction, User
from rest_framework import status
from datetime import datetime, timedelta, timezone

def SchedulerBalance():
    transactions = Transaction.objects.all()  
    for transaction in transactions:
        if datetime.now(tz=timezone(timedelta(hours=-3))).date() >= transaction.payday and transaction.transaction_state == 'Started':
            place = Place.objects.get(pk=transaction.id_place)
            id_owner = place.id_owner
            owner = User.objects.get(pk=id_owner)
            new_balance = owner.balance + transaction.payment
            owner.balance = new_balance
            owner.save()
            transaction.transaction_state = "Finished"
            transaction.save()
