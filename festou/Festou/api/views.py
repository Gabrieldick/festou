from rest_framework import generics
from .actions import chargeback, login_user
from .manager import create_place, create_score, create_transaction, create_user, delete_place, edit_place, get_user_transaction_made, get_user_transactions_received
from .searches import place, place_id, score_id, transaction_id, user_id
from .serializer import CreatePlaceSerializer, SearchPlaceSerializer
from rest_framework.views import APIView

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