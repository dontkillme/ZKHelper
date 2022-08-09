from django.contrib import admin
from apps.logistic.models import MagazineItem


class AdminView(admin.ModelAdmin):
    pass


admin.site.register(MagazineItem, AdminView)
