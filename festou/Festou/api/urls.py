from django.urls import path
from api import views

urlpatterns = [
    path('user', views.UserView.as_view()),
    path('v1/signup', views.CreateUserView.as_view()),
    path('v1/login', views.LoginUserView.as_view()),
    path('v1/search', views.PlaceSearchView.as_view()),
    path('v1/place', views.CreatePlaceView.as_view()),
    path('v1/EditPlace/<int:place_id>',views.EditPlace.as_view()),
    path('v1/delete_place/<int:place_id>/', views.DeletePlace.as_view()),
    path('v1/place/<int:id>', views.SearchPlaceId.as_view()),
    path('v1/user/<int:id>', views.SearchUserId.as_view()),
    path('v1/transaction/', views.CreateTransaction.as_view()), 
    path('v1/transaction/<int:id>', views.SearchTransactionId.as_view()), 
    path('v1/payment/<int:id_transaction>', views.SchedulerTransaction.as_view()),
    path('v1/chargeback/', views.Chargeback.as_view()),  
    path('v1/create_score/', views.CreateScore.as_view()),
    path('v1/get_score/<int:id_place>/', views.GetScoreByID.as_view()),
]

#path('v1/balance/<int:id>/<str:balance>/<int:dia>/<int:mes>/<int:ano>', views.SchedulerBalance.as_view()),