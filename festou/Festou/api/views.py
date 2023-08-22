from rest_framework import generics
from .serializer import CreatePlaceSerializer, SearchPlaceSerializer, LoginUserSerializer, CreateScoreSerializer, CreateTransactionSerializer, CreateUserSerializer, EditUserSerializer, WithdrawMoneySerializer, CreateChargebackSerializer, IdListSerializer
from rest_framework.views import APIView
from .actions import *
from .searches import * 
from .manager import *
from rest_framework.parsers import JSONParser, MultiPartParser

class CreateUserView(generics.CreateAPIView): 
    serializer_class = CreateUserSerializer
    def post(self, request):
        return create_user(self, request)

class CreatePlaceView(generics.CreateAPIView):  #Funcionamento análogo à outras funções de criação
    serializer_class = CreatePlaceSerializer
    parser_classes = [JSONParser, MultiPartParser]
    def post(self, request):
        return create_place(self, request)
    
class CreatePlace(APIView):

    parser_classes = [JSONParser, MultiPartParser]

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = CreatePlaceSerializer(data=request.data)

        if serializer.is_valid():
            # Acesse os dados do serializer
            name = serializer.validated_data.get("name")
            price = serializer.validated_data.get("price")
            location = serializer.validated_data.get("location")
            capacity = serializer.validated_data.get("capacity")
            id_owner = serializer.validated_data.get("id_owner")
            description = serializer.validated_data.get("description")
            terms_of_use = serializer.validated_data.get("terms_of_use")
            checked = 0

            # Acesse as imagens do serializer
            image_1 = serializer.validated_data.get('image_1')
            image_2 = serializer.validated_data.get('image_2')
            image_3 = serializer.validated_data.get('image_3')

            # Verifique se já existe um lugar com a mesma localização
            queryset = Place.objects.filter(location=location)
            if queryset.exists():
                return Response({'description': 'Location already linked to an existing place. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)

            # Crie uma instância de Place com os dados e imagens
            place = Place(
                name=name,
                price=price,
                location=location,
                capacity=capacity,
                description=description,
                id_owner=id_owner,
                terms_of_use=terms_of_use,
                checked=checked,
                total_score=0,
                score=0,
                avaliations=0,
                image_1=image_1,
                image_2=image_2,
                image_3=image_3
            )

            # Salve o lugar no banco de dados
            place.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
class CreateTransaction(APIView): #Funcionamento análogo à outras funções de criação
    serializer_class = CreateTransactionSerializer
    def post(self, request):
        return create_transaction(self, request)

class PlaceSearchView(generics.ListCreateAPIView):
    serializer_class = SearchPlaceSerializer
    def post(self, request):
        return place(self, request)

class IdPlaceListView(generics.ListCreateAPIView):
    serializer_class = IdListSerializer
    def post(self, request):
        return id_place_list(self, request)
    
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
    def get(self, request, id_transaction):
        return chargeback(self, request, id_transaction)

class LoginUserView(generics.CreateAPIView): 
    serializer_class = LoginUserSerializer
    def post(self, request):
        return login_user(self, request)

