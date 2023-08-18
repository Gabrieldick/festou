from rest_framework import serializers
from .models import User, Place, Transaction, Score

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','cpf','phone','password','birthdate','bank','account','agency')

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','cpf','phone','password','birthdate','bank','account','agency')

class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id_client', 'id_place', 'initial_date', 'final_date')

class ReportTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id_place', 'initial_date', 'final_date', 'transaction_date', 'transaction_state', 'payment')
class CreateChargebackSerializer(serializers.Serializer):
    id_transaction = serializers.IntegerField()

class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password')

class IdUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name')

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id','name','price','location','capacity','description')

class SearchPlaceSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    capacity = serializers.IntegerField(allow_null=True)
    initial_price = serializers.FloatField(allow_null=True)
    final_price = serializers.FloatField(allow_null=True)
    initial_date = serializers.CharField(allow_null=True)
    final_date = serializers.CharField(allow_null=True)
    score = serializers.FloatField(allow_null=True)

class CreatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('name','price','location','capacity','description', 'terms_of_use')

class DeletePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id')

class CreateScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('id_place', 'id_client', 'score', 'description')