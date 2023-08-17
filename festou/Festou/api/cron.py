from rest_framework.response import Response
from .models import Place, Transaction, User
from rest_framework import status
from datetime import datetime

def SchedulerBalance():
    transactions = Transaction.objects.all()  
    for transaction in transactions:
        if datetime.now().date() >= transaction.payday.date():
            place = Place.objects.get(pk=transaction.id_place)
            id_owner = place.id_owner
            owner = User.objects.get(pk=id_owner)
            new_balance = owner.balance + transaction.payment
            owner.balance = new_balance
            owner.save()
            transaction.transactionState = "Finished"
            transaction.save()
            return Response({'message': f'User balance updated: {new_balance}'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Payday not reached yet.'}, status=status.HTTP_400_BAD_REQUEST)
    
