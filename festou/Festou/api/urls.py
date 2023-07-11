from django.urls import path
from .views import UserView, CreateUserView, LoginUserView, CreatePlaceView, PlaceSearchView

urlpatterns = [
    path('user', UserView.as_view()),
    path('v1/signup', CreateUserView.as_view()),
    path('v1/login', LoginUserView.as_view()),
    path('v1/search', PlaceSearchView.as_view()),
    path('v1/register-place', CreatePlaceView.as_view())
]