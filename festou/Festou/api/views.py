from django.shortcuts import render
from rest_framework import generics, status
from .serializer import UserSerializer, CreateUserSerializer, LoginUserSerializer, IdUserSerializer, PlaceSerializer, CreatePlaceSerializer, SearchPlaceSerializer
from .models import User, Place
import json
from rest_framework.views import APIView
from rest_framework.response import Response
import hashlib

# Create your views here.

#retorna todos os usuários
class UserView(generics.ListCreateAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
            queryset = User.objects.filter(cpf = cpf)
            if queryset.exists():
                return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = User.objects.filter(email = email)
            if queryset.exists():
                return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
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
                        agency = agencia
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
                    return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'description': 'Email or password not found. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
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
            price = serializer.validated_data.get("price") 
            location = serializer.validated_data.get("location")
            capacity = serializer.validated_data.get("capacity")
            score = serializer.validated_data.get("score")
            descrpition = serializer.validated_data.get("descrpition")
            queryset = Place.objects.filter(location = location)
            if queryset.exists():
                return Response({'description': 'Location already linked to an existing place. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'description': 'Location already linked to an existing place. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            place = Place(
                        name = name,
                        price = price,
                        price = price,
                        location = location,
                        capacity = capacity,
                        score = score,
                        descrpition = descrpition
                        )
            place.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
    
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
        return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class PlaceView(generics.ListCreateAPIView): 
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
        
    
    
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