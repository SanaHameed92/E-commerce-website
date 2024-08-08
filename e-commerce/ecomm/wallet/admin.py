from django.contrib import admin
from . models import WalletTransaction,ReturnRequest

class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('order__order_number',)

admin.site.register(ReturnRequest, ReturnRequestAdmin)


admin.site.register(WalletTransaction)
# Register your models here.
