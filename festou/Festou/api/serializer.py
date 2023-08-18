from rest_framework import serializers
from .models import User, Place, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','firstName','lastName','email','cpf','phone','password','birthdate','bank','account','agency')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('firstName','lastName','email','cpf','phone','password','birthdate','bank','account','agency')

class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id_client', 'id_place', 'initialDate', 'payday', 'finalDate', 'price', 'payment')

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
        fields = ('id','name','price','location','capacity','score','descrpition')

class SearchPlaceSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    capacity = serializers.IntegerField(allow_null=True)
    initial_price = serializers.FloatField(allow_null=True)
    final_price = serializers.FloatField(allow_null=True)
    id_user = serializers.IntegerField(allow_null=True)

class CreatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('name','price','location','capacity','score','descrpition')

class DeletePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id')