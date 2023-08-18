from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework import generics, status
from .serializer import UserSerializer, CreateUserSerializer, LoginUserSerializer, IdUserSerializer, PlaceSerializer, CreatePlaceSerializer, SearchPlaceSerializer, CreateTransactionSerializer, CreateChargebackSerializer, CreateScoreSerializer, ReportTransactionSerializer
from .models import User, Place, Transaction, Score
import json
from rest_framework.views import APIView
from rest_framework.response import Response
import hashlib
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
#from background_task import background

# Create your views here.

class CreateUserView(generics.CreateAPIView): 
    serializer_class = CreateUserSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): #verifica se o JSON enviado condiz com os dados esperados
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
            queryset = User.objects.filter(cpf = cpf)  #Realização de verificações para não serem criadas duas contas com mesmo email ou cpf
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
            user.save() #Salva o usuário na database
            return Response(IdUserSerializer(user).data,status=status.HTTP_201_CREATED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginUserView(generics.CreateAPIView): 
    serializer_class = LoginUserSerializer
    def post(self, request): 
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(): #verifica se o JSON enviado condiz com os dados esperados
            email = serializer.validated_data.get("email")  
            senha = serializer.validated_data.get("password")
            senha = encrypt_password(senha)
            queryset = User.objects.filter(email = email) #Filtra usuário pelo email, dado que é único por conta
            if queryset.exists():
                user = queryset[0]
                if user.password == senha:
                    return Response(IdUserSerializer(user).data, status=status.HTTP_200_OK)
                else:
                    return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class CreatePlaceView(generics.CreateAPIView):  #Funcionamento análogo à outras funções de criação
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
            id_owner = serializer.validated_data.get("id_owner")
            description = serializer.validated_data.get("description")
            termsofuse = serializer.validated_data.get("termsofuse")
            queryset = Place.objects.filter(location = location)
            checked = Null
            if queryset.exists():
                return Response({'description': 'Location already linked to an existing place. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            place = Place(
                        name = name,
                        price = price,
                        location = location,
                        capacity = capacity,
                        description = description,
                        id_owner = id_owner,
                        termsofuse = termsofuse,
                        checked = checked
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
            places = Place.objects.filter(name__contains=nome) #filtra todos os objetos da classe Place que contenham parte ou todo o nome passado

            location = serializer.validated_data.get("location")
            places_loc = Place.objects.filter(location__contains=location)

            initialPrice = serializer.validated_data.get("initialPrice")
            places_initPrice = Place.objects.filter(price__gte=initialPrice) #filtra todos os objetos com price maior que o preço inicial

            finalPrice = serializer.validated_data.get("finalPrice")
            places_finalPrice = Place.objects.filter(price__lte=finalPrice) #filtra todos os objetos com price menor que o preço final

            capacity = serializer.validated_data.get("capacity")
            places_capacity = Place.objects.filter(capacity__gte=capacity)

            #verifica se as informações devem ser utilizadas e pega apenas a intersecção dos locais filtrados
            places = places.intersection(places_loc)
            if initialPrice != 0:
                places = places.intersection(places_initPrice)
            if finalPrice != 0:
                places = places.intersection(places_finalPrice)
            if capacity != 0:
                places = places.intersection(places_capacity)

            serializer = PlaceSerializer(places, many=True)

            return Response(serializer.data, status=200)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class SearchUserId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        try: 
            search = User.objects.get(pk = id)
            response_data = UserSerializer(search).data
            return JsonResponse(response_data, status=200)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
class SearchPlaceId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        try: 
            search = Place.objects.get(pk = id)
            response_data = PlaceSerializer(search).data      
            return JsonResponse(response_data, status=200)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The place does not exist'}, status=status.HTTP_404_NOT_FOUND)
                
class SearchTransactionId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        try: 
            search = Transaction.objects.get(pk = id)
            response_data = CreateTransactionSerializer(search).data      
            return JsonResponse(response_data)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The place does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class UserTransactionsMade(generics.ListCreateAPIView): #Transações na qual o usuário é o cliente
    def get(self, request, id, *args, **kwargs):
        try: 
            Transactions = Transaction.objects.filter(id_client__contains = id)
            serializer = ReportTransactionSerializer(Transactions, many=True)
            return Response(serializer.data, status=200)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class UserTransactionsReceived(generics.ListCreateAPIView): #Transações na qual o usuário é o anunciante
    def get(self, request, id, *args, **kwargs):
        try: 
            Transactions = Transaction.objects.filter(id_advertiser__contains = id)
            serializer = ReportTransactionSerializer(Transactions, many=True)
            return Response(serializer.data, status=200)
        except Place.DoesNotExist: 
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

class CreateTransaction(generics.ListCreateAPIView): #Funcionamento análogo à outras funções de criação
    serializer_class = CreateTransactionSerializer
    queryset = Transaction.objects.all()

    def post(self, request):     #initialDate and finalDate is datatime
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_client = serializer.validated_data.get("id_client")
            id_place = serializer.validated_data.get("id_place")
            id_advertiser = serializer.validated_data.get("id_advertiser")
            initialDate = serializer.validated_data.get("initialDate")
            finalDate = serializer.validated_data.get("finalDate")


            days_to_subtract = 7 #Quantidade de dias antes do evento que será liberado o dinheiro 
            payday = initialDate - timedelta(days=days_to_subtract)

            atual_place = Place.objects.get(pk = id_place)
            price = atual_place.price

            delta_time = finalDate - initialDate
            payment =(int(delta_time.days)+1) * price

            transaction = Transaction(
                id_place = id_place, 
                id_client = id_client,
                id_advertiser = id_advertiser,
                price = price,
                initialDate = initialDate,
                finalDate = finalDate,
                payday = payday,
                payment = payment,
                transactionDate = datetime.now().date(),
                transactionState = "Started"
                )
            transaction.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class Balance(generics.ListCreateAPIView): #Atualiza o valor em conta do usuário
    def addBalance(self, id, balance): 
        user = User.objects.get(pk = id)
        if user.balance == None:
                user.balance = 0.0   
        user.balance = user.balance + float(balance)
        user.save()
'''
@background(schedule=5)  # A tarefa será verificada a cada hora
def SchedulerBalance():
    completed_transactions = Transaction.objects.filter(payday__gte=datetime.now().date())  
    for transactions in completed_transactions:
        if transactions.transactionState == "Started":
            id_owner = Place.objects.get(pk=transactions.id_place).id_owner
            Balance.addBalance(id_owner, transactions.payment)
            transactions.transactionState = "Finished"
'''
class SchedulerTransaction(APIView):
    def get(self, request, id_transaction, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(pk=id_transaction)  
            # Verificar se o payday foi atingido e transicionar de local o dinheiro
            if datetime.now().date() >= transaction.payday.date():
                id_owner = transaction.id_advertiser
                owner = User.objects.get(pk=id_owner)
                new_balance = owner.balance + transaction.payment
                owner.balance = new_balance
                owner.save()
                return Response({'message': f'User balance updated: {new_balance}'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Payday not reached yet.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Transaction.DoesNotExist:
            return Response({'message': 'Transaction not found.'}, status=status.HTTP_404_NOT_FOUND)

    '''
    def get(self, request, id_transaction, *args, **kwargs):
        transaction = Transaction.objects.get(pk=id_transaction)  
        if transaction.payday.date() <= datetime.now().date():
            id_owner = Place.objects.get(pk=transaction.id_place).id_owner
            Balance.addBalance(self, id=id_owner, balance=transaction.payment)
            transaction.delete()
    '''
class Chargeback(APIView):
    serializer_class = CreateChargebackSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id_transaction = serializer.validated_data.get('id_transaction')
            if id_transaction is None:            #verifica se está recebendo as informações necessárias
                return Response({'error': 'id_transaction is required.'}, status=400)
            try: #verifica se esta transação existe
                transaction = Transaction.objects.get(pk=id_transaction)
            except Transaction.DoesNotExist:
                return Response({'error': 'Transaction not found.'}, status=404)

            if datetime.now().date() > transaction.payday.date() and transaction.transactionState == 'Started':
                client = get_object_or_404(User, pk=transaction.id_client)
                Balance.addBalance(self,id=transaction.id_client, balance=transaction.payment) #devolve o dinheiro para o comprador e altera o status da transação

                transaction.transactionState = "Canceled"
                transaction.save()

                return Response({'message': 'Chargeback successful.'}, status=200)
            else:
                return Response({'message': 'Cannot perform chargeback after payday.'}, status=400)
        else:
            return Response(serializer.errors, status=400)

class EditPlace(APIView):
    def put(self, request, place_id):
        try:
            place = Place.objects.get(pk=place_id)
            
            # Verificar se o usuário é o proprietário do lugar
            if place.id_owner != request.user.id:
                return Response({'message': 'You are not the owner of this place.'}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = PlaceSerializer(place, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Place.DoesNotExist:
            return Response({'message': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)

class DeletePlace(APIView):
    def delete(self, request, place_id):
        try:
            place = Place.objects.get(pk=place_id)
            
            # Verificar se o usuário é o proprietário do lugar
            if place.id_owner != request.user.id:
                return Response({'message': 'You are not the owner of this place.'}, status=status.HTTP_403_FORBIDDEN)
            
            place.delete()
            return Response({'message': 'Place deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        
        except Place.DoesNotExist:
            return Response({'message': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)

class CreateScore(APIView):
    serializer_class = CreateScoreSerializer
    def post(self, request):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            idClient = serializer.validated_data.get("idClient")
            description = serializer.validated_data.get("description")
            score = serializer.validated_data.get("score")
            idPlace = serializer.validated_data.get("idPlace")

            score_obj = Score(
                idClient = idClient, 
                description = description,
                score = score,
                idPlace = idPlace,
                )
            score_obj.save()
            return Response({'message': 'Score created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetScoreByID(APIView):
    def get(self, request, id_place):
        try:
            scores = Score.objects.filter(idPlace=id_place)
            score_data = [{"name": User.objects.get(pk=score.idClient).firstName, "description": score.description, "score": score.score} for score in scores]
            return JsonResponse(score_data, safe=False)
        except Score.DoesNotExist:
            return JsonResponse({'message': 'No scores found for the specified place ID.'}, status=status.HTTP_404_NOT_FOUND)

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
