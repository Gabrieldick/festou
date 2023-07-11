from rest_framework import serializers
from .models import User, Place

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','firstName','lastName','email','cpf','phone','password','birthdate','bank','account','agency')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName','lastName','email','cpf','phone','password','birthdate','bank','account','agency')

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')

class IdUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','firstName')

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id','name','initialPrice','finalPrice','initialDate','finalDate','location','capacity','score','descrpition')

class SearchPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('filter','name','initialPrice','finalPrice','initialDate','finalDate','location','capacity','score')

class CreatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('name','initialPrice','finalPrice','initialDate','finalDate','location','capacity','score','descrpition')