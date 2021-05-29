from django.urls import path

from . import views

urlpatterns = [
    path('bills/', views.api_bills),
    path('bill/<int:bill_id>/', views.api_bill),
    path('boleto/<int:boleto_id>/', views.api_boleto),
    path('movimentacoes/', views.api_movimentacoes),
    path('movimentacao/<int:mov_id>/', views.api_movimentacao),
]
