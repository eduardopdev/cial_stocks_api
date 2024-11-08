from django.urls import path
from .views import StocksView

urlpatterns = [
    path('', StocksView.as_view(), name='stocks'),  # GET and SET endpoints
    path('<str:stock_ticker>', StocksView.as_view(), name="stocks_post")
]