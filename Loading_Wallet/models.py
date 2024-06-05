
from django.db import models
import uuid


class Accounts(models.Model):
    account_name = models.CharField(max_length=255, blank=True,)
    account_number = models.CharField(unique=True, max_length=255)
    account_type = models.TextField()  
    account_status = models.TextField() 
    actual_balance = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    available_balance = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  
    updatedat = models.DateTimeField(db_column='updatedAt')  
    customerid = models.UUIDField(db_column='CustomerId') 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdby = models.CharField(db_column='createdBy', max_length=255) 

    class Meta:
        managed = False
        db_table = 'Accounts'


class Sequelizemeta(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'SequelizeMeta'


class Customers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(db_column='firstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(max_length=255, blank=True, null=True)
    identificationdocument = models.CharField(db_column='IdentificationDocument', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(max_length=255, blank=True, null=True)
    age = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    middlename = models.CharField(db_column='middleName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    identificationtype = models.CharField(db_column='identificationType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    walletaccount = models.CharField(db_column='walletAccount', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdby = models.CharField(db_column='createdBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    updatedby = models.CharField(db_column='updatedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customers'


# class Loans(models.Model):
#     id = models.UUIDField(blank=True, null=True)
#     loan_amount = models.IntegerField(blank=True, null=True)
#     loan_currency = models.CharField(max_length=255, blank=True, null=True)
#     loan_interest = models.IntegerField(blank=True, null=True)
#     customerid = models.UUIDField(db_column='CustomerId', blank=True, null=True)  # Field name made lowercase.
#     createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
#     updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'loans'


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    credited_Account = models.CharField(max_length=255)
    debited_Account = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    external_Reference = models.CharField(max_length=255)
    internal_Reference = models.CharField(max_length=255)
    transaction_Date = models.DateTimeField()
    transaction_Type = models.CharField(max_length=1, choices=[("C", "Credit"), ("D", "Debit")])
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updatedAt = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        db_table = 'transactions'


class Users(models.Model):
    id = models.UUIDField(blank=True, primary_key=True, default=uuid.uuid4)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt') 
    updatedat = models.DateTimeField(db_column='updatedAt') 
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


# class Wallets(models.Model):
#     id = models.UUIDField(blank=True, null=True)
#     wallet_balance = models.IntegerField(blank=True, null=True)
#     wallet_currency = models.CharField(max_length=255, blank=True, null=True)
#     customerid = models.UUIDField(db_column='CustomerId', blank=True, null=True)  # Field name made lowercase.
#     createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
#     updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'wallets'
