from rest_framework import generics
from .serializer import CreatePlaceSerializer, SearchPlaceSerializer, LoginUserSerializer, CreateScoreSerializer, CreateTransactionSerializer, CreateUserSerializer, EditUserSerializer, WithdrawMoneySerializer, CreateChargebackSerializer
from rest_framework.views import APIView
from .actions import *
from .searches import * 
from .manager import *

class CreateUserView(generics.CreateAPIView): 
    serializer_class = CreateUserSerializer
    def post(self, request):
        return create_user(self, request)

class CreatePlaceView(generics.CreateAPIView):  #Funcionamento análogo à outras funções de criação
    serializer_class = CreatePlaceSerializer
    def post(self, request):
        return create_place(self, request)

class CreateTransaction(APIView): #Funcionamento análogo à outras funções de criação
    serializer_class = CreateTransactionSerializer
    def post(self, request):
        return create_transaction(self, request)

class PlaceSearchView(generics.ListCreateAPIView):
    serializer_class = SearchPlaceSerializer
    def post(self, request):
        return place(self, request)

class SearchUserId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        return user_id(self, request, id)

class UserPlacesId(generics.ListCreateAPIView):
    def get(self, request, id, *args, **kwargs):
        return user_places_id(self, request, id)

class UserTransactionsId(APIView):
    def get(self, request, id, *args, **kwargs):
        return user_transactions_id(self, request, id)

class PlaceTransactionsId(APIView):
    def get(self, request, id, *args, **kwargs):
        return place_transactions_id(self, request, id)


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

class EditUser(APIView):
    serializer_class = EditUserSerializer
    def put(self, request, user_id):
        return edit_user(self, request, user_id)
    
class WithdrawMoney(APIView):
    serializer_class = WithdrawMoneySerializer
    def post(self, resquet):
        return withdraw_money(self, resquet)

class EditPlace(APIView):
    serializer_class = PlaceSerializer
    def put(self, request, place_id):
        return edit_place(self, request, place_id)

class DeletePlace(APIView):
    def delete(self, request, place_id):
        return delete_place(self, request, place_id)

class CreateScore(APIView):
    serializer_class = CreateScoreSerializer
    def post(self, request):
        return create_score(self, request)

class GetScoreByID(APIView):
    def get(self, request, id_place):
        return score_id(self, request, id_place)

class Chargeback(APIView):
    serializer_class = CreateChargebackSerializer
    def post(self, request):
        return chargeback(self, request)

class LoginUserView(generics.CreateAPIView): 
    serializer_class = LoginUserSerializer
    def post(self, request):
        return login_user(self, request)
