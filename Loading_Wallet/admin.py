from django.contrib import admin
from .models import Accounts, Sequelizemeta, Customers, Transactions

admin.site.register(Accounts)
admin.site.register(Sequelizemeta)
admin.site.register(Customers)
admin.site.register(Transactions)

