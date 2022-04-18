from django.contrib import admin

from .models import Week, Shopping, Money, Hesab,MainHesab, LastHesab

admin.site.register(Week)
admin.site.register(Shopping)
admin.site.register(Money)
admin.site.register(Hesab)
admin.site.register(MainHesab)
admin.site.register(LastHesab)