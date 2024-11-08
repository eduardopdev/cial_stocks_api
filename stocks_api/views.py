from django.core.cache import cache
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework import status
from .models import Stock
from functions import scraping_marketwatch, get_stock_daily
from datetime import datetime, timedelta
from decimal import Decimal

class StocksView(APIView):
    def get(self, request):
        stock_ticker = request.GET.get('ticker', None)
        if stock_ticker == None:
            return Response({"message": "No ticker provided"}, status=status.HTTP_404_NOT_FOUND)
        cache_key = stock_ticker
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        
        performance_dict, competitors_list = scraping_marketwatch(stock_ticker)
        stock_qs = Stock.objects.filter(company_code=stock_ticker)
        if stock_qs.exists():
            stock = stock_qs.first()
            today = datetime.now()
            year, month, day = str(today.year), \
                               "0"+str(today.month) if today.month<10 else str(today.month), \
                               "0"+str(today.day) if today.day<10 else str(today.day)
            stock_daily = get_stock_daily(stock_ticker, year+"-"+month+"-"+day)
            print(stock_daily)
            if "open" not in stock_daily.keys():
                today = datetime.today()
                new_york = today - timedelta(hours=2)
                if new_york.day != today.day:
                    yesterday = today - timedelta(days=2)
                else:
                    yesterday = today - timedelta(days=1)
                year, month, day = str(yesterday.year), \
                                   "0"+str(yesterday.month) if yesterday.month<10 else str(yesterday.month), \
                                   "0"+str(yesterday.day) if yesterday.day<10 else str(yesterday.day)
                stock_daily = get_stock_daily(stock_ticker, year+"-"+month+"-"+day)
                response_data = {
                    "status": "NA",
                    "purchased_amount": stock.purchased_amount,
                    "purchased_status": stock.purchased_status,
                    "company_code": stock.company_code,
                    "company_name": stock.company_name,
                    "stock_values": {
                        "open": stock_daily["open"],
                        "high": stock_daily["high"],
                        "low": stock_daily["low"],
                        "close": stock_daily["close"]
                    },
                    "performance_data": {
                        "five_days": performance_dict["5 Day"],
                        "one_month": performance_dict["1 Month"],
                        "three_months": performance_dict["3 Month"],
                        "year_to_date": performance_dict["YTD"],
                        "one_year": performance_dict["1 Year"]
                    },
                    "competitors": competitors_list
                }
        
        if not stock_qs.exists():
            today = datetime.now()
            year, month, day = str(today.year), \
                               "0"+str(today.month) if today.month<10 else str(today.month), \
                               "0"+str(today.day) if today.day<10 else str(today.day)
            stock_daily = get_stock_daily(stock_ticker, year+"-"+month+"-"+day)
            if "open" not in stock_daily.keys():
                today = datetime.today()
                new_york = today - timedelta(hours=2)
                if new_york.day != today.day:
                    yesterday = today - timedelta(days=2)
                else:
                    yesterday = today - timedelta(days=1)
                year, month, day = str(yesterday.year), \
                                   "0"+str(yesterday.month) if yesterday.month<10 else str(yesterday.month), \
                                   "0"+str(yesterday.day) if yesterday.day<10 else str(yesterday.day)
                stock_daily = get_stock_daily(stock_ticker, year+"-"+month+"-"+day)
            try:
                response_data = {
                    "status": "NA",
                    "purchased_amount": Decimal(0),
                    "purchased_status": "NA",
                    "company_code": stock_ticker,
                    "company_name": "NA",
                    "stock_values": {
                        "open": stock_daily["open"],
                        "high": stock_daily["high"],
                        "low": stock_daily["low"],
                        "close": stock_daily["close"]
                    },
                    "performance_data": {
                        "five_days": performance_dict["5 Day"],
                        "one_month": performance_dict["1 Month"],
                        "three_months": performance_dict["3 Month"],
                        "year_to_date": performance_dict["YTD"],
                        "one_year": performance_dict["1 Year"]
                    },
                    "competitors": competitors_list
                }
            except KeyError:
                return Response({"resource error": f"No stock named {stock_ticker}"}, status=status.HTTP_404_NOT_FOUND)
        cache.set(cache_key, response_data, timeout=300)
        return Response(response_data, status=status.HTTP_200_OK)
    
    def post(self, request, stock_ticker):
        performance_dict, competitors_list = scraping_marketwatch(stock_ticker)
        amount = request.POST.get('amount', None)
        if not amount:
            amount = Decimal(0)
        try:
            amount = Decimal(amount)
        except:
            amount = 0
        stock_qs = Stock.objects.filter(company_code=stock_ticker)
        if stock_qs.exists():
            stock = stock_qs.first()
            stock.purchased_amount += Decimal(amount)
            stock.save()
            return Response({"message": f"{amount} units of stock {stock_ticker} added to your stock record"}, status=status.HTTP_201_CREATED)
        if not stock_qs.exists():
            today = datetime.now()
            new_york = today - timedelta(hours=2)
            if new_york.day != today.day:
                yesterday = today - timedelta(days=2)
            else:
                yesterday = today - timedelta(days=1)
            year, month, day = str(today.year), \
                               "0"+str(today.month) if today.month<10 else str(today.month), \
                               "0"+str(today.day) if today.day<10 else str(today.day)
            stock_daily = get_stock_daily(stock_ticker, year+"-"+month+"-"+day)
            if "open" not in stock_daily.keys():
                today = datetime.today()
                yesterday = today - timedelta(days=1)
                year, month, day = str(yesterday.year), \
                                   "0"+str(yesterday.month) if yesterday.month<10 else str(yesterday.month), \
                                   "0"+str(yesterday.day) if yesterday.day<10 else str(yesterday.day)
                stock_daily = get_stock_daily(stock_ticker, year+"-"+month+"-"+day)
            try:
                response_data = {
                    "status": "NA",
                    "purchased_amount": Decimal(0),
                    "purchased_status": "NA",
                    "company_code": stock_ticker,
                    "company_name": "NA",
                    "stock_values": {
                        "open": stock_daily["open"],
                        "high": stock_daily["high"],
                        "low": stock_daily["low"],
                        "close": stock_daily["close"]
                    },
                    "performance_data": {
                        "five_days": performance_dict["5 Day"],
                        "one_month": performance_dict["1 Month"],
                        "three_months": performance_dict["3 Month"],
                        "year_to_date": performance_dict["YTD"],
                        "one_year": performance_dict["1 Year"]
                    },
                    "competitors": competitors_list
                }
            except KeyError:
                return Response({"resource error": f"No stock named {stock_ticker}"}, status=status.HTTP_404_NOT_FOUND)
            stock = Stock(**response_data)
            stock.save()
            return Response({"message": f"{amount} units of stock {stock_ticker} added to your stock record"}, status=status.HTTP_201_CREATED)