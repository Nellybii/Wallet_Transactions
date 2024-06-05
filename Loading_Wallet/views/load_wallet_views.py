import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.db import transaction
from django.conf import settings
from ..models import Transactions, Customers, Accounts
from requests.auth import HTTPBasicAuth
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
def load_wallet_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        customer_id = data.get('customerid')
        amount = float(data.get('amount'))
        transaction_type = data.get('transaction_type')
        external_reference = data.get('external_reference')
        internal_reference = data.get('internal_reference')
        transaction_date = data.get('transaction_date')
        
        response, status = update_account_and_create_transaction(
            customer_id=customer_id, amount=amount, 
            transaction_type=transaction_type,
            external_reference=external_reference, 
            internal_reference=internal_reference,
            transaction_date=transaction_date, 
            
        )

        return JsonResponse(response, status=status)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def mpesa_validation(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        logger.info("Mpesa Validation Data: %s", data)
        response = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(response)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

@csrf_exempt
def mpesa_confirmation(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        logger.info("Mpesa Validation Data: %s", data)
        
        try:
            amount = float(data['TransAmount'])
            external_reference = data['TransID']
            internal_reference = data["BillRefNumber"]
            transaction_date_str = data['TransTime']
            transaction_date = datetime.strptime(transaction_date_str, "%Y%m%d%H%M%S")
            customer_msisdn = data['MSISDN']
        except KeyError as e:
            logger.error("Missing key in MPesa confirmation data: %s", e)
            return JsonResponse({'error': f"Missing key: {e}"}, status=400)
        except ValueError as e:
            logger.error("Invalid date format in MPesa confirmation data: %s", e)
            return JsonResponse({'error': f"Invalid date format: {e}"}, status=400)

        try:
            customer = Customers.objects.get(phone=customer_msisdn)
        except Customers.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=400)

        response, status = update_account_and_create_transaction(
            customer_id=customer.id, 
            amount=amount, 
            transaction_type='C',
            external_reference=external_reference, 
            internal_reference=internal_reference,
            transaction_date=transaction_date

        )

        return JsonResponse(response, status=status)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

def get_all_transactions(request):
    transactions = Transactions.objects.all()
    data = [{'id': t.id, 'credited_account': t.credited_Account, 'debited_account': t.debited_Account,
             'amount': t.amount, 'external_reference': t.external_Reference,
             'internal_reference': t.internal_Reference, 'transaction_type': t.transaction_Type,
             'transaction_date': t.transaction_Date} for t in transactions]
    return JsonResponse({'transactions': data})

def update_account_and_create_transaction(customer_id, amount, transaction_type, external_reference, internal_reference, transaction_date):
    try:
        account = Accounts.objects.get(customerid=customer_id)
    except Accounts.DoesNotExist:
        return {'error': 'Account not found'}, 400

    with transaction.atomic():
        if transaction_type == 'C':
            account.available_balance += Decimal(amount)
        elif transaction_type == 'D':
            if account.available_balance < Decimal(amount):
                return {'error': 'Insufficient balance'}, 400
            account.available_balance -= Decimal(amount)
        account.save()

        transaction_record = Transactions.objects.create(
            credited_Account=account.account_number if transaction_type == 'C' else 'M-Pesa',
            debited_Account='M-Pesa' if transaction_type == 'C' else account.account_number,
            amount=Decimal(amount),
            external_Reference=external_reference,
            internal_Reference=internal_reference,
            transaction_Type=transaction_type,
            transaction_Date=transaction_date,
        )

    return {'success': True, 'transaction_id': transaction_record.id}, 200

def generate_access_token():
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise Exception("Failed to generate access token")

def register_urls():
    access_token = generate_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": settings.MPESA_CONFIRMATION_URL,
        "ValidationURL": settings.MPESA_VALIDATION_URL
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to register URLs")

