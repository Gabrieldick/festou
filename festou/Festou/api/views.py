from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import generics, status
from .serializer import UserSerializer, CreateUserSerializer, LoginUserSerializer, IdUserSerializer, PlaceSerializer, CreatePlaceSerializer, SearchPlaceSerializer, CreateTransactionSerializer, CreateChargebackSerializer
from .models import User, Place, Transaction
import json
from rest_framework.views import APIView
from rest_framework.response import Response
import hashlib
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
from background_task import background

# Create your views here.

#retorna todos os usuários
class UserView(generics.ListCreateAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    for user in User.objects.all():
        user.balance = 0.0

class CreateUserView(generics.CreateAPIView): 
    serializer_class = CreateUserSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            nome = serializer.validated_data.get("firstName")
            sobrenome = serializer.validated_data.get("lastName") 
            email = serializer.validated_data.get("email")
            cpf = serializer.validated_data.get("cpf")
            celular = serializer.validated_data.get("phone")
            senha = serializer.validated_data.get("password")
            senha = encrypt_password(senha)
            data_de_aniversario = serializer.validated_data.get("birthdate")
            banco = serializer.validated_data.get("bank")
            conta = serializer.validated_data.get("account")
            agencia = serializer.validated_data.get("agency")
            balance = 0.0
            queryset = User.objects.filter(cpf = cpf)
            if queryset.exists():
                return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = User.objects.filter(email = email)
            if queryset.exists():
                return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            user = User(
                        firstName = nome,
                        lastName = sobrenome,
                        email = email,
                        cpf = cpf,
                        phone = celular,
                        password = senha,
                        birthdate = data_de_aniversario,
                        bank = banco,
                        account = conta,
                        agency = agencia,
                        balance = balance
                        )
            user.save()
            return Response(IdUserSerializer(user).data,status=status.HTTP_201_CREATED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(generics.CreateAPIView): 
    serializer_class = LoginUserSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")  
            senha = serializer.validated_data.get("password")
            senha = encrypt_password(senha)
            queryset = User.objects.filter(email = email)
            if queryset.exists():
                user = queryset[0]
                if user.password == senha:
                    return Response(IdUserSerializer(user).data, status=status.HTTP_200_OK)
                else:
                    return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    

class CreatePlaceView(generics.CreateAPIView): 
    serializer_class = CreatePlaceSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            price = serializer.validated_data.get("price") 
            location = serializer.validated_data.get("location")
            capacity = serializer.validated_data.get("capacity")
            score = serializer.validated_data.get("score")
            descrpition = serializer.validated_data.get("descrpition")
            termsofuse = serializer.validated_data.get("termsofuse")
            queryset = Place.objects.filter(location = location)
            if queryset.exists():
                return Response({'description': 'Location already linked to an existing place. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            place = Place(
                        name = name,
                        price = price,
                        location = location,
                        capacity = capacity,
                        score = score,
                        descrpition = descrpition,
                        termsofuse = termsofuse
                        )
            place.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request):
        Place.objects.all().delete()
        return Response(status=status.HTTP_423_LOCKED)
    
class PlaceSearchView(generics.ListCreateAPIView):
    serializer_class = SearchPlaceSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            nome = serializer.validated_data.get("name")
            places = Place.objects.filter(name__contains=nome)
            location = serializer.validated_data.get("location")
            places_loc = Place.objects.filter(location__contains=location)
            places = places.intersection(places_loc)
            serializer = PlaceSerializer(places, many=True)
            return Response(serializer.data, status=200)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class PlaceView(generics.ListCreateAPIView): 
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

class SearchUserId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        try: 
            search = User.objects.get(pk = id)
            response_data = UserSerializer(search).data
            return JsonResponse(response_data)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class SearchPlaceId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        try: 
            search = Place.objects.get(pk = id)
            response_data = PlaceSerializer(search).data      
            return JsonResponse(response_data)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The place does not exist'}, status=status.HTTP_404_NOT_FOUND)

class CreateTransaction(generics.ListCreateAPIView):
    serializer_class = CreateTransactionSerializer
    queryset = Transaction.objects.all()

    def post(self, request):     #initialDate and finalDate is datatime
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_client = serializer.validated_data.get("id_client")
            id_place = serializer.validated_data.get("id_place")
            initialDate = serializer.validated_data.get("initialDate")
            finalDate = serializer.validated_data.get("finalDate")

            days_to_subtract = 7
            payday = initialDate - timedelta(days=days_to_subtract)

            atual_place = Place.objects.get(pk = id_place)
            price = atual_place.price

            delta_time = finalDate - initialDate
            payment =(int(delta_time.days)+1) * price

            transaction = Transaction(
                id_place = id_place, 
                id_client = id_client,
                price = price,
                initialDate = initialDate,
                finalDate = finalDate,
                payday = payday,
                payment = payment
                )
            transaction.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class Balance(generics.ListCreateAPIView):
    def get(self, request, id, balance, *args, **kwargs):
        try:
            search = User.objects.get(pk = id)
            search.balance = float(balance) 
            data_response = {
                "balance" : float(balance)
            }
            return JsonResponse(data_response)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)  

    def addBalance(self, id, balance):
        search = User.objects.get(pk = id)
        if search.balance == None:
                search.balance = 0.0   
        search.balance = search.balance + float(balance)
        search.save()

@background(schedule=5)  # A tarefa será verificada a cada hora
def SchedulerBalance():
    completed_transactions = Transaction.objects.filter(payday__gte=datetime.now().date())  
    for transactions in completed_transactions:
        id_owner = Place.objects.get(pk=transactions.id_place).id_owner
        Balance.addBalance(id_owner, transactions.payment)
        transactions.delete()

class Chargeback(APIView):
    serializer_class = CreateChargebackSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_transaction = serializer.validated_data.get('id_transaction')
            if id_transaction is None:            
                id_transaction = request.data.get('id_transaction')
                return Response({'error': 'id_transaction is required.'}, status=400)
            try:
                transaction = Transaction.objects.get(pk=id_transaction)
            except Transaction.DoesNotExist:
                return Response({'error': 'Transaction not found.'}, status=404)

            if datetime.now().date() < transaction.payday.date():
                client = get_object_or_404(User, pk=transaction.id_client)
                Balance.addBalance(self,id=transaction.id_client, balance=transaction.payment)

                transaction.delete()

                return Response({'message': 'Chargeback successful.'}, status=200)
            else:
                return Response({'message': 'Cannot perform chargeback after payday.'}, status=400)
        else:
            return Response(serializer.errors, status=400)

def encrypt_password(password):

    # Criando um objeto hash SHA-256
    hash_object = hashlib.sha256()

    # Convertendo a senha em bytes
    password_bytes = password.encode('utf-8')

    # Atualizando o objeto hash com a senha
    hash_object.update(password_bytes)

    # Obtendo a senha criptografada em formato hexadecimal
    hashed_password = hash_object.hexdigest()
    return hashed_password

