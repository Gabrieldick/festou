from rest_framework import status
from .models import User, Transaction
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime
from .serializer import IdUserSerializer
from .searches import * 
from .manager import *
import hashlib

def login_user(self, request):
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get("email")  
        senha = serializer.validated_data.get("password")
        senha = encrypt_password(senha)
        queryset = User.objects.filter(email = email) #Filtra usuário pelo email, dado que é único por conta
        if queryset.exists():
            user = queryset[0]
            if user.blocked == False:
                if user.password == senha:
                    return Response(IdUserSerializer(user).data, status=status.HTTP_200_OK)
                else:
                    return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'description': 'You are blocked.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

def withdraw_money(self, request):
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
        id_client = serializer.validated_data.get('id_client')
        amount = serializer.validated_data.get('amount')
        if id_client is None: #verifica se está recebendo as informações necessárias
            return Response({'error': 'id_client is required.'}, status=400)
        try: #verifica se este usuário existe
            user = User.objects.get(pk=id_client)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        if user.balance >= amount and amount > 0:
            user.balance -= amount
            user.save()
            return Response({'message': 'Withdraw successful.'}, status=200)
        else:
            return Response({'message': 'Amount invalid .'}, status=400)
    else:
        return Response(serializer.errors, status=400)

def chargeback(self, request, id_transaction):
    if id_transaction is None: #verifica se está recebendo as informações necessárias
        return Response({'error': 'id_transaction is required.'}, status=400)
    try: #verifica se esta transação existe
        transaction = Transaction.objects.get(pk=id_transaction)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=404)
    if datetime.now().date() < transaction.payday and transaction.transaction_state == 'Started':
        add_balance(self,id=transaction.id_client, balance=transaction.payment) #devolve o dinheiro para o comprador e altera o status da transação
        transaction.transaction_state = "Canceled"
        transaction.save()
        return Response({'message': 'Chargeback successful.'}, status=200)
    else:
        return Response({'message': 'Cannot perform chargeback after payday.'}, status=400)
    

def report_user(self, request, id_transaction):
    if id_transaction is None: #verifica se está recebendo as informações necessárias
        return Response({'error': 'id_transaction is required.'}, status=400)
    try: #verifica se esta transação existe
        transaction = Transaction.objects.get(pk=id_transaction)
    except Transaction.DoesNotExist:
        return Response({'error': 'Transaction not found.'}, status=404)
    client = get_object_or_404(User, pk=transaction.id_client)
    client.reported = True
    client.save()
    return Response({'message': 'Successful report.'}, status=200)

def encrypt_password(password):
    hash_object = hashlib.sha256() # Criando um objeto hash SHA-256
    password_bytes = password.encode('utf-8')# Convertendo a senha em bytes
    hash_object.update(password_bytes)# Atualizando o objeto hash com a senha
    hashed_password = hash_object.hexdigest()# Obtendo a senha criptografada em formato hexadecimal
    return hashed_password
