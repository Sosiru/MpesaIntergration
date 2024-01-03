import json, datetime

import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode

from base.backend.service import PaymentTransactionService, StateService, CustomerCredentialService, CustomerService

# Applies for LipaNaMpesaOnline Payment method
def generate_pass_key(credentials):
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = credentials.shortcode + credentials.pass_key + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')


def get_token(credentials):
    api_url = "{}{}".format(credentials.safaricom_api, credentials.auth_url)
    r = requests.get(api_url, auth=HTTPBasicAuth(credentials.consumer_key, credentials. consumer_secret))
    if r.status_code == 200:
        jonresponse = json.loads(r.content)
        access_token = jonresponse['access_token']
        print(access_token)
        return access_token
    elif r.status_code == 400:
        print('Invalid credentials.')
        return False


def sendSTK(customer_identifier, phone_number, amount, orderId=0, transaction_id=None):
    customer = CustomerService().get(identifier=customer_identifier)
    print(customer)
    credentials = CustomerCredentialService().get(customer=customer)
    print(credentials)
    code = credentials.shortcode# shortcode or SHORT_CODE
    party_b = credentials.till_number
    account_number = credentials.account_number
    access_token = get_token(credentials)
    if access_token is False:
        raise Exception("Invalid Consumer key or secret or both")

    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")

    s = code + credentials.pass_key + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')

    api_url = "{}/mpesa/stkpush/v1/processrequest".format(credentials.safaricom_api)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }

    transaction_type = credentials.trx_type or "CustomerBuyGoodsOnline"
    # If account number is set, change transaction type to paybill
    if account_number:
        transaction_type = "CustomerPayBillOnline"
    elif transaction_type == "CustomerPayBillOnline" and account_number == None:
        account_number = phone_number

    request = {
        "BusinessShortCode": int(code),
        "Password": encoded,
        "Timestamp": time_now,
        "TransactionType": transaction_type,
        "Amount": str(int(amount)),
        "PartyA": phone_number,
        "PartyB": party_b,
        "PhoneNumber": phone_number,
        "CallBackURL": "{}/v1/billing/confirm/".format(credentials.host_name),
        "AccountReference": account_number or code,
        "TransactionDesc": "{}".format(phone_number)
    }

    print("request is :",request)
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    print("response is",json_response)
    if json_response.get('ResponseCode'):
        if json_response["ResponseCode"] == "0":
            checkout_id = json_response["CheckoutRequestID"]
            if transaction_id:
                transaction = PaymentTransactionService().filter(id=transaction_id).first()
                transaction.checkout_request_id = checkout_id
                transaction.save()
                return transaction.id
            else:
                transaction = PaymentTransactionService().create(
                    phone_number=phone_number, checkout_request_id=checkout_id,
                    amount=amount,order_id=orderId, state=StateService().get(name="Completed"))
                transaction.save()
                return transaction.id
    else:
        raise Exception("Error sending MPesa stk push", json_response)


def check_payment_status(checkout_request_id, customer_identifier):
    customer = CustomerService().get(identifier=customer_identifier)
    credentials = CustomerCredentialService().get(customer=customer)
    code = credentials.shortcode
    access_token = get_token(credentials)
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%I%S")
    s = code + credentials.pass_key + time_now
    encoded = b64encode(s.encode('utf-8')).decode('utf-8')
    api_url = "{}/mpesa/transactionstatus/v1/query".format(credentials.safaricom_api)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json",
    }
    request = {
        "BusinessShortCode": code,
        "Password": encoded,
        "Timestamp": time_now,
        "CheckoutRequestID": checkout_request_id
    }
    response = requests.post(api_url, json=request, headers=headers)
    json_response = json.loads(response.text)
    if 'ResponseCode' in json_response and json_response["ResponseCode"] == "0":
        requestId = json_response.get('CheckoutRequestID')
        transaction = PaymentTransactionService().get(
            checkout_request_id=requestId)
        if transaction:
            PaymentTransactionService().update(pk=transaction.id, state=StateService().get(name="Completed"))
            transaction.save()
        else:
            PaymentTransactionService().update(pk=transaction.id,  state=StateService().get(name="Completed"))
            transaction.save()
        result_code = json_response['ResultCode']
        response_message = json_response['ResultDesc']
        return {
            "code": result_code,
            "response": result_code == "0",
            "transaction_status": transaction.state.name,
            "message": response_message
        }
    else:
        raise Exception("Error checking transaction status", json_response)
