from django.db import models
from copy import deepcopy

stock_values_dict = {
   "open": 0.0,
   "high": 0.0,
   "low": 0.0,
   "close": 0.0
}

performance_data_dict = {
    "five_days": 0.0,
    "one_month": 0.0,
    "three_months": 0.0,
    "year_to_date": 0.0,
    "one_year": 0.0
}

competitors_dict = {
    "name": "",
    "market_cap": {
        "currency": "",
        "value": 0.0
    }
}

def get_stock_values_dict():
    return deepcopy(stock_values_dict)

def get_performance_data_dict():
    return deepcopy(performance_data_dict)

def get_competitors_dict():
    return deepcopy(competitors_dict)

class Stock(models.Model):
    status = models.CharField(null=False, default="NA", max_length=16, blank=False)
    purchased_amount = models.DecimalField(null=False, max_digits=10, decimal_places=0, blank=False)
    purchased_status = models.CharField(null=False, default="NA", max_length=32, blank=False)
    company_code = models.CharField(null=False, default="NA", max_length=32, blank=False)
    company_name = models.CharField(null=False, default="NA", max_length=128, blank=False)
    stock_values = models.JSONField(null=False, default=get_stock_values_dict, blank=False)
    performance_data = models.JSONField(null=False, default=get_performance_data_dict, blank=False)
    competitors = models.JSONField(null=False, default=get_competitors_dict, blank=False)
    request_data = models.DateField(auto_now_add=True)

class RequestLog(models.Model):
    level = models.CharField(null=True, max_length=50, default="INFO")
    message = models.TextField()
    request_tmstp = models.DateTimeField(null=True, auto_now_add=True)