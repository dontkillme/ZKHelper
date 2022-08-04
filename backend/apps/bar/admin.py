from django.contrib import admin
from apps.bar.models import BarReceipt, BarAccount, BarItem, BarItemCategory, BarReceiptItem


class AdminView(admin.ModelAdmin):
    pass


class BarReceiptAdmin(admin.ModelAdmin):
    list_filter = ('items', )
    filter_horizontal = ('items', )


admin.site.register(BarReceipt, BarReceiptAdmin)
admin.site.register(BarAccount, AdminView)
admin.site.register(BarItem, AdminView)
admin.site.register(BarItemCategory, AdminView)
admin.site.register(BarReceiptItem, AdminView)
