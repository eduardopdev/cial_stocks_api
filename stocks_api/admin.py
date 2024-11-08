from django.contrib import admin
from .models import Stock, RequestLog
# Register your models here.

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["status", "purchased_amount", "company_code", "request_data"]

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ["level", "message", "request_tmstp"]