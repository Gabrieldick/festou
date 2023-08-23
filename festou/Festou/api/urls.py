from django.urls import path
from api import views

urlpatterns = [
    path('v1/signup', views.CreateUserView.as_view()),
    path('v1/editUser/<int:user_id>',views.EditUser.as_view()),
    path('v1/userPlaces/<int:id>', views.UserPlacesId.as_view()),
    path('v1/userTransactions/<int:id>', views.UserTransactionsId.as_view()),
    path('v1/user/<int:id>', views.SearchUserId.as_view()),
    path('v1/reportUser/<int:id_transaction>', views.ReportUser.as_view()),
    
    path('v1/login', views.LoginUserView.as_view()),
    path('v1/search', views.PlaceSearchView.as_view()),

    path('v1/place', views.CreatePlaceView.as_view()),
    path('v1/editPlace/<int:place_id>',views.EditPlace.as_view()),
    path('v1/deletePlace/<int:place_id>', views.DeletePlace.as_view()),
    path('v1/place/<int:id>', views.SearchPlaceId.as_view()),
    path('v1/placeTransactions/<int:id>', views.PlaceTransactionsId.as_view()),
    path('v1/IdListPlaces', views.IdPlaceListView.as_view()),

    path('v1/withdraw', views.WithdrawMoney.as_view()),

    path('v1/transaction', views.CreateTransaction.as_view()), 
    path('v1/transaction/<int:id>', views.SearchTransactionId.as_view()),
    path('v1/getTransactionsMade/<int:id>', views.UserTransactionsMade.as_view()),
    path('v1/getTransactionsReceived/<int:id>', views.UserTransactionsReceived.as_view()),
    
    path('v1/chargeback/<int:id_transaction>', views.Chargeback.as_view()),  

    path('v1/createScore', views.CreateScore.as_view()),
    path('v1/getScore/<int:id_place>', views.GetScoreByID.as_view()),    
]