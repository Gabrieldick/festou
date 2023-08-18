import hashlib
from rest_framework import generics
from .serializer import CreatePlaceSerializer, SearchPlaceSerializer
from rest_framework.views import APIView
from .actions import *
from .searches import * 
from .manager import *

class CreateUserView(generics.CreateAPIView): 
    def post(self, request):
        return create_user(self, request)

class CreatePlaceView(generics.CreateAPIView):  #Funcionamento análogo à outras funções de criação
    serializer_class = CreatePlaceSerializer
    def post(self, request):
        return create_place(self, request)

class CreateTransaction(generics.ListCreateAPIView): #Funcionamento análogo à outras funções de criação
    def post(self, request):
        return create_transaction(self, request)

class PlaceSearchView(generics.ListCreateAPIView):
    serializer_class = SearchPlaceSerializer
    def post(self, request):
        return place(self, request)

class SearchUserId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        return user_id(self, request, id)

class SearchPlaceId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        return place_id(self, request, id)

class SearchTransactionId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        return transaction_id(self, request, id)

class UserTransactionsMade(generics.ListCreateAPIView): #Transações na qual o usuário é o cliente
    def get(self, request, id, *args, **kwargs):
        return get_user_transaction_made(self, request, id)
    
class UserTransactionsReceived(generics.ListCreateAPIView): #Transações na qual o usuário é o anunciante
    def get(self, request, id, *args, **kwargs):
        return get_user_transactions_received(self, request, id)

class EditPlace(APIView):
    def put(self, request, place_id):
        edit_place(self, request, place_id)

class DeletePlace(APIView):
    def delete(self, request, place_id):
        delete_place(self, request, place_id)

class CreateScore(APIView):
    def post(self, request):
        create_score(self, request)

class GetScoreByID(APIView):
    def get(self, request, id_place):
        score_id(self, request, id_place)

class Chargeback(APIView):
    def post(self, request):
        chargeback(self, request)

class LoginUserView(generics.CreateAPIView): 
    def post(self, request):
        login_user(self, request)

def encrypt_password(password):
    hash_object = hashlib.sha256() # Criando um objeto hash SHA-256
    password_bytes = password.encode('utf-8')# Convertendo a senha em bytes
    hash_object.update(password_bytes)# Atualizando o objeto hash com a senha
    hashed_password = hash_object.hexdigest()# Obtendo a senha criptografada em formato hexadecimal
    return hashed_password