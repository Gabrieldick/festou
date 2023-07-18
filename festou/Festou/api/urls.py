from django.urls import path
from api import views

urlpatterns = [
    path('user', views.UserView.as_view()),
    path('v1/signup', views.CreateUserView.as_view()),
    path('v1/login', views.LoginUserView.as_view()),
    path('v1/search', views.PlaceSearchView.as_view()),
    path('v1/place', views.CreatePlaceView.as_view())
]