from datetime import datetime
from .manager import parse_date
from .serializer import UserSerializer, PlaceSerializer, CreateTransactionSerializer
from .models import User, Place, Transaction, Score
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
import base64

def place(self, request):
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():

        nome = serializer.validated_data.get("name")
        places = Place.objects.filter(name__contains=nome) #filtra todos os objetos da classe Place que contenham parte ou todo o nome passado

        location = serializer.validated_data.get("location")
        places_loc = Place.objects.filter(location__contains=location) 

        initialPrice = serializer.validated_data.get("initial_price")
        places_initPrice = Place.objects.filter(price__gte=initialPrice) #filtra todos os objetos com price maior que o preço inicial

        finalPrice = serializer.validated_data.get("final_price")
        places_finalPrice = Place.objects.filter(price__lte=finalPrice) #filtra todos os objetos com price menor que o preço final

        capacity = serializer.validated_data.get("capacity")
        places_capacity = Place.objects.filter(capacity__gte=capacity)

        id_user = serializer.validated_data.get("id_user")
        places_user = Place.objects.filter(id_owner=id_user) 

        score = serializer.validated_data.get("score")
        places_score = Place.objects.filter(score__gte=score)

        initial_date_string = serializer.validated_data.get("initial_date")
        final_date_string = serializer.validated_data.get("final_date")
        

        places_valid = Place.objects.filter(checked=1) 
        places = places.intersection(places_loc)
        places = places.intersection(places_valid)

        
        #filtra os Places que não têm transações não canceladas em initial e final date
        if parse_date(initial_date_string) is not None and parse_date(final_date_string) is not None:
            if parse_date(initial_date_string) >= datetime.now().date() and parse_date(final_date_string) >= parse_date(initial_date_string):

                overlapping_transactions = Transaction.objects.filter(
                    initial_date__lte=final_date_string,
                    final_date__gte=initial_date_string
                ).exclude(transaction_state="Canceled")

                print (overlapping_transactions)

                overlapping_transaction_ids = []
                for transaction in overlapping_transactions:
                    overlapping_transaction_ids.append(transaction.id_place)

                places_with_overlapping_transactions = Place.objects.filter(pk__in=overlapping_transaction_ids)
                places = places.difference(places_with_overlapping_transactions)

        #verifica se as informações devem ser utilizadas e pega apenas a intersecção dos locais filtrados

        if initialPrice != 0:
            places = places.intersection(places_initPrice)
        if finalPrice != 0:
            places = places.intersection(places_finalPrice)
        if capacity != 0:
            places = places.intersection(places_capacity)
        if score != 0:
            places = places.intersection(places_score)

        serializer = PlaceSerializer(places, many=True)

         # Lista para armazenar os lugares com imagens em base64
        places_with_images_base64 = []

        for place in places:

            # Obtenha os caminhos dos arquivos de imagem dos campos do modelo
            image_1_path = place.image_1.path if place.image_1 else ''


            # Leitura dos dados das imagens (assumindo que sejam arquivos locais)
            image_1_data = open(image_1_path, 'rb').read() if image_1_path else None


            # Codifique as imagens em base64 para incluí-las no JSON
            image_1_base64 = base64.b64encode(image_1_data).decode('utf-8') if image_1_data else ''


            # Adicione as imagens aos dados de resposta
            response_data = PlaceSerializer(place).data
            response_data['image_1'] = image_1_base64

            
            # Adicione o lugar modificado à lista
            places_with_images_base64.append(response_data)

        return Response(places_with_images_base64, status=200)
    return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

def id_place_list(self, request):
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
        
        id_list = serializer.validated_data.get("id_list")
        if len(id_list) == 0:
            return Response(status=200)
        
        places = Place.objects.filter(id = id_list[0])
        for id_place in id_list:
            place = Place.objects.filter(id = id_place)
            places = places.union(place)

        serializer = PlaceSerializer(places, many=True)

        places_with_images_base64 = []

        for place in places:

            # Obtenha os caminhos dos arquivos de imagem dos campos do modelo
            image_1_path = place.image_1.path if place.image_1 else ''


            # Leitura dos dados das imagens (assumindo que sejam arquivos locais)
            image_1_data = open(image_1_path, 'rb').read() if image_1_path else None


            # Codifique as imagens em base64 para incluí-las no JSON
            image_1_base64 = base64.b64encode(image_1_data).decode('utf-8') if image_1_data else ''


            # Adicione as imagens aos dados de resposta
            response_data = PlaceSerializer(place).data
            response_data['image_1'] = image_1_base64

            
            # Adicione o lugar modificado à lista
            places_with_images_base64.append(response_data)

        return Response(places_with_images_base64, status=200)
    return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

def user_id(self, request, id):
    try: 
        search = User.objects.get(pk = id)
        response_data = UserSerializer(search).data
        return JsonResponse(response_data, status=200)
    except User.DoesNotExist: 
        return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)

def user_places_id(self, request, id):
    try: 
        places = Place.objects.filter(id_owner=id)
        response_data = PlaceSerializer(places, many=True).data
        return JsonResponse(response_data, status=200, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)

def place_id(self, request, id):
    try: 
        search = Place.objects.get(pk=id)

        # Obtenha os caminhos dos arquivos de imagem dos campos do modelo
        image_1_path = search.image_1.path if search.image_1 else ''


        # Leitura dos dados das imagens (assumindo que sejam arquivos locais)
        image_1_data = open(image_1_path, 'rb').read() if image_1_path else None


        # Codifique as imagens em base64 para incluí-las no JSON
        image_1_base64 = base64.b64encode(image_1_data).decode('utf-8') if image_1_data else ''


        # Adicione as imagens aos dados de resposta
        response_data = PlaceSerializer(search).data
        response_data['image_1'] = image_1_base64

        return JsonResponse(response_data, status=200)
    except Place.DoesNotExist: 
        return JsonResponse({'message': 'The place does not exist'}, status=status.HTTP_404_NOT_FOUND)


def transaction_id(self,request, id):
    try: 
        search = Transaction.objects.get(pk = id)
        response_data = CreateTransactionSerializer(search).data      
        return JsonResponse(response_data)
    except Place.DoesNotExist: 
        return JsonResponse({'message': 'The place does not exist'}, status=status.HTTP_404_NOT_FOUND)

def user_transactions_id(self, request, id):
    try: 
        transactions = Transaction.objects.filter(id_client=id)
        response_data = CreateTransactionSerializer(transactions, many=True).data
        return JsonResponse(response_data, status=200, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The User does not exist'}, status=status.HTTP_404_NOT_FOUND)

def place_transactions_id(self, request, id):
    try: 
        transactions = Transaction.objects.filter(id_place=id)
        response_data = CreateTransactionSerializer(transactions, many=True).data
        return JsonResponse(response_data, status=200, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The Place does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
def score_id(self, request, id_place):
    try:
        scores = Score.objects.filter(id_place=id_place)
        score_data = [{"name": User.objects.get(pk=score.id_client).first_name, "description": score.description, "score": score.score} for score in scores]
        return JsonResponse(score_data, safe=False)
    except Score.DoesNotExist:
        return JsonResponse({'message': 'No scores found for the specified place ID.'}, status=status.HTTP_404_NOT_FOUND)