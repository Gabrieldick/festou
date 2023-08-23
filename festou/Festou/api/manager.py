from .serializer import  IdUserSerializer, ReportTransactionSerializer
from .models import User, Place, Transaction, Score
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import hashlib

def parse_date(date: str) -> datetime.date:
    try:
        return datetime.strptime(date, '%d/%m/%Y').date()
    except ValueError: 
        return None

def create_user(self, request): 
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(): #verifica se o JSON enviado condiz com os dados esperados
        nome = serializer.validated_data.get("first_name")
        sobrenome = serializer.validated_data.get("last_name") 
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
        blocked = False
        queryset = User.objects.filter(cpf = cpf) #Realização de verificações para não serem criadas duas contas com mesmo email ou cpf
        if queryset.exists():
            return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        queryset = User.objects.filter(email = email)
        if queryset.exists():
            return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User(
                    first_name = nome,
                    last_name = sobrenome,
                    email = email,
                    cpf = cpf,
                    phone = celular,
                    password = senha,
                    birthdate = data_de_aniversario,
                    bank = banco,
                    account = conta,
                    agency = agencia,
                    balance = balance,
                    blocked = blocked
                    )
        user.save() #Salva o usuário na database
        return Response(IdUserSerializer(user).data,status=status.HTTP_201_CREATED)
    return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)    

def edit_user(self, request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            queryset = User.objects.filter(email = user.email)
            if queryset.exists():
                return Response({'description': 'CPF or Email already linked to an existing account. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Place.DoesNotExist:
        return Response({'message': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)

def add_balance(self, id, balance): 
        user = User.objects.get(pk = id)
        if user.balance == None:
                user.balance = 0.0   
        user.balance = user.balance + float(balance)
        user.save()

def create_place(self, request):
    if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

    serializer = self.serializer_class(data=request.data)

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

def edit_place(self, request, place_id):
    try:
        place = Place.objects.get(pk=place_id)
        serializer = self.serializer_class(place, data=request.data)
        if serializer.is_valid():
            # Acesse os dados do serializer
            name = serializer.validated_data.get("name")
            price = serializer.validated_data.get("price")
            capacity = serializer.validated_data.get("capacity")
            description = serializer.validated_data.get("description")
            terms_of_use = serializer.validated_data.get("terms_of_use")

            # Acesse as imagens do serializer
            image_1 = serializer.validated_data.get('image_1')
            image_2 = serializer.validated_data.get('image_2')
            image_3 = serializer.validated_data.get('image_3')

            print (image_1)
            place.name=name
            place.price=price
            place.capacity=capacity
            place.description=description
            place.terms_of_use=terms_of_use
            place.image_1=image_1
            place.image_2=image_2
            place.image_3=image_3
            # Salve o lugar no banco de dados
            place.save()

            return Response(status=status.HTTP_201_CREATED)
    except Place.DoesNotExist:
        return Response({'message': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)

def delete_place(self, request, place_id):
    try:
        place = Place.objects.get(pk=place_id)
        place.delete()
        return Response({'message': 'Place deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    except Place.DoesNotExist:
        return Response({'message': 'Place not found.'}, status=status.HTTP_404_NOT_FOUND)

def create_transaction(self, request):
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
        id_client = serializer.validated_data.get("id_client")
        id_place = serializer.validated_data.get("id_place")
        initial_date = serializer.validated_data.get("initial_date")
        final_date = serializer.validated_data.get("final_date")

        #vendo se faz sentido 
        if parse_date(initial_date) < timezone.now().date() or parse_date(final_date) < parse_date(initial_date):
            return Response({'description': 'Invalid date range...'}, status=status.HTTP_400_BAD_REQUEST)
        overlapping_transactions = Transaction.objects.filter(
            id_place=id_place,
            initial_date__lte=parse_date(final_date),
            final_date__gte=parse_date(initial_date),
        ).exclude(transaction_state="Canceled")
        
        if overlapping_transactions.exists():
            return Response({'description': 'Date conflict with existing transactions...'}, status=status.HTTP_400_BAD_REQUEST)

        days_to_subtract = 7 #Quantidade de dias antes do evento que será liberado o dinheiro 
        payday = parse_date(initial_date) - timedelta(days=days_to_subtract)
        atual_place = Place.objects.get(pk = id_place)
        price = atual_place.price
        id_advertiser = atual_place.id_owner
        delta_time = parse_date(final_date) - parse_date(initial_date)
        payment =(int(delta_time.days)+1) * price
        transaction = Transaction(
            id_place = id_place, 
            id_client = id_client,
            id_advertiser = id_advertiser,
            price = price,
            initial_date = parse_date(initial_date),
            final_date = parse_date(final_date),
            payday = payday,
            payment = payment,
            transaction_date = datetime.now().date(),
            transaction_state = "Started",
            name = atual_place.name,
            location = atual_place.location
            )
        transaction.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({'description': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

def get_user_transaction_made(self, request, id):
    try: 
        Transactions = Transaction.objects.filter(id_client__contains = id)
        serializer = ReportTransactionSerializer(Transactions, many=True)
        return Response(serializer.data, status=200)
    except Place.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

def get_user_transactions_received(self, request, id):
    try: 
        Transactions = Transaction.objects.filter(id_advertiser__contains = id)
        serializer = ReportTransactionSerializer(Transactions, many=True)
        return Response(serializer.data, status=200)
    except Place.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

def create_score(self, request):
    if not self.request.session.exists(self.request.session.session_key):
        self.request.session.create()
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
        idClient = serializer.validated_data.get("id_client")
        description = serializer.validated_data.get("description")
        score = serializer.validated_data.get("score")
        idPlace = serializer.validated_data.get("id_place")
        score_obj = Score(
            id_client = idClient, 
            description = description,
            score = score,
            id_place = idPlace,
            )
        score_obj.save()
        update_place_score(idPlace, score)
        return Response({'message': 'Score created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_place_score(id_place, score):
    try:
        place = Place.objects.get(pk=id_place)
        place.score = (place.total_score + score)/float(place.avaliations+1)
        place.total_score += score
        place.avaliations += 1
        place.save()
        return
    except ObjectDoesNotExist:
        return 0
    
def encrypt_password(password):
    hash_object = hashlib.sha256() # Criando um objeto hash SHA-256
    password_bytes = password.encode('utf-8')# Convertendo a senha em bytes
    hash_object.update(password_bytes)# Atualizando o objeto hash com a senha
    hashed_password = hash_object.hexdigest()# Obtendo a senha criptografada em formato hexadecimal
    return hashed_password