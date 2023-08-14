from django.urls import path
from api import views

urlpatterns = [
    path('user', views.UserView.as_view()),
    path('v1/signup', views.CreateUserView.as_view()),
    path('v1/login', views.LoginUserView.as_view()),
    path('v1/search', views.PlaceSearchView.as_view()),
    path('v1/place', views.CreatePlaceView.as_view()),
    path('v1/place/<int:id>', views.SearchPlaceId.as_view()),  
    path('v1/user/<int:id>', views.SearchUserId.as_view()),    
    path('v1/balance/<int:id>/<str:balance>', views.setBalance.as_view()),    
]
