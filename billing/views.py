# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse

from base.backend.service import PaymentTransactionService, StateService
from base.backend.transaction_log_base import TransactionLogBase
from base.backend.utils.common import get_request_data, get_client_ip
from billing.backend.LipaNaMpesaOnline import sendSTK, check_payment_status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from .models import PaymentTransaction
from django.http import JsonResponse
from rest_framework.permissions import AllowAny


# Create your views here.
class PaymentTranactionView(ListCreateAPIView):
    def post(self, request):
        return HttpResponse("OK", status=200)


class SubmitView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        transaction = None
        try:
            source_ip = get_client_ip(request)
            transaction = transaction = TransactionLogBase().log_transaction(
                "SendSTK", request=request, source_ip=source_ip)
            if not transaction:
                return {"code": "200.006.001", 'message': 'Error creating transaction'}
            data = get_request_data(request)
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            customer_identifier = data.get('identifier')
            print(phone_number)
            entity_id = 0
            if data.get('entity_id'):
                entity_id = data.get('entity_id')
            # paybill_account_number = None
            # if data.get('paybill_account_number'):
            #     paybill_account_number = data.get('paybill_account_number')
            transaction_id = sendSTK(customer_identifier, phone_number, amount, entity_id)
            # b2c()
            message = {"status": "ok", "transaction_id": transaction_id}
            TransactionLogBase().complete_transaction(
                transaction, response="100.000.000", description="Success")
            return Response(message, status=HTTP_200_OK)
        except Exception as ex:
            TransactionLogBase().mark_transaction_failed(
                transaction, response="999.999.999", description=str(ex))
            return JsonResponse({"code": "100.000.001"})


class CheckTransactionOnline(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        transaction = None
        try:
            source_ip = get_client_ip(request)
            transaction = transaction = TransactionLogBase().log_transaction(
                "CheckTransactionOnline", request=request, source_ip=source_ip)
            if not transaction:
                return {"code": "200.006.001", 'message': 'Error creating transaction'}
            data = get_request_data(request)
            trans_id = data.get('transaction_id')
            customer_identifier = data.get('identifier')
            transaction = PaymentTransactionService().get(id=trans_id)
            if transaction.checkout_request_id:
                status_response = check_payment_status(transaction.checkout_request_id, customer_identifier)
                TransactionLogBase().complete_transaction(
                    transaction, response="100.000.000", description="Success")
                return JsonResponse(
                    status_response, status=200)
            else:
                TransactionLogBase().mark_transaction_failed(
                    transaction, response="999.999.999", description="not found")
                return JsonResponse({
                    "message": "Server Error. Transaction not found",
                    "status": False
                }, status=400)
        except Exception as ex:
            TransactionLogBase().mark_transaction_failed(
                transaction, response="999.999.999", description=str(ex))
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class CheckTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        transaction = None
        try:
            source_ip = get_client_ip(request)
            transaction = transaction = TransactionLogBase().log_transaction(
                "CheckTransaction", request=request, source_ip=source_ip)
            data = get_request_data(request)
            trans_id = data.get('transaction_id')
            transaction = PaymentTransactionService().get(id=trans_id)
            if transaction:
                TransactionLogBase().complete_transaction(
                    transaction, response="100.000.000", description="Success")
                return JsonResponse({
                    "message": "ok",
                    "finished": transaction.is_finished,
                    "successful": transaction.is_successful
                },
                    status=200)
            else:
                # TODO : Edit order if no transaction is found
                TransactionLogBase().mark_transaction_failed(
                    transaction, response="999.999.999", description="not found")
                return JsonResponse({
                    "message": "Error. Transaction not found",
                    "status": False
                },
                    status=400)
        except Exception as ex:
            TransactionLogBase().mark_transaction_failed(
                transaction, response="999.999.999", description=str(ex))
            return JsonResponse({
                "message": "Server Error. Transaction not found",
                "status": False
            },
                status=400)


class RetryTransaction(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        transaction = None
        try:
            source_ip = get_client_ip(request)
            transaction = TransactionLogBase().log_transaction(
                "RetryTransaction", request=request, source_ip=source_ip)
            data = get_request_data(request)
            trans_id = data.get('transaction_id')
            transaction = PaymentTransactionService().filter(id=trans_id).get()
            if transaction and transaction.state == StateService().get(name="Completed"):
                TransactionLogBase().complete_transaction(
                    transaction, response="100.000.000", description="Success")
                return JsonResponse({
                    "message": "ok",
                    # "finished": transaction.,
                    "status": transaction.state.name
                },
                    status=200)
            else:
                response = sendSTK(
                    phone_number=transaction.phone_number,
                    amount=transaction.amount,
                    orderId=transaction.order_id)
                TransactionLogBase().complete_transaction(
                    transaction, response="100.000.000", description="Success")
                return JsonResponse({
                    "message": "ok",
                    "transaction_id": response
                },
                    status=200)

        except Exception as ex:
            TransactionLogBase().mark_transaction_failed(
                transaction, response="999.999.999", description=str(ex))
            return JsonResponse({
                "message": "Error. Transaction not found",
                "status": False
            },
                status=400)


class ConfirmView(APIView):
    permission_classes = [AllowAny, ]
    def post(self, request):
        # save the data
        transaction = None
        try:
            source_ip = get_client_ip(request)
            transaction = TransactionLogBase().log_transaction(
                "ConfirmTransaction", request=request, source_ip=source_ip)
            request_data = json.dumps(request.data)
            request_data = json.loads(request_data)
            body = request_data.get('Body')
            resultcode = body.get('stkCallback').get('ResultCode')
            receipt_number = ""
            # Perform your processing here e.g. print it out...
            if resultcode == 0:
                print('Payment successful')
                requestId = body.get('stkCallback').get('CheckoutRequestID')
                metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
                for data in metadata:
                    print(data)
                    if data.get('Name') == "MpesaReceiptNumber":
                        receipt_number = data.get('Value')
                transaction = PaymentTransactionService().get(
                    checkout_request_id=requestId)
                if transaction:
                    print(transaction)
                    PaymentTransactionService().update(
                        pk=transaction.id,
                         receipt_number=receipt_number)
            else:
                print('unsuccessfull')
                requestId = body.get('stkCallback').get('CheckoutRequestID')
                transaction = PaymentTransactionService().get(
                    checkout_request_id=requestId)
                if transaction:
                    transaction.state = StateService().get(name="Failed")
                    transaction.save()

            # Prepare the response, assuming no errors have occurred. Any response
            # other than a 0 (zero) for the 'ResultCode' during Validation only means
            # an error occurred and the transaction is cancelled
            message = {
                "ResultCode": 0,
                "ResultDesc": "The service was accepted successfully",
                "ThirdPartyTransID": "1237867865"
            }

            # Send the response back to the server
            TransactionLogBase().complete_transaction(
                transaction, response="100.000.000", description="Success")
            return Response(message, status=HTTP_200_OK)
        except Exception as ex:
            TransactionLogBase().mark_transaction_failed(
                transaction, response="999.999.999", description=str(ex))
            return JsonResponse({
                "message": "Error. Transaction not found",
                "status": False
            },
                status=400)

    def get(self, request):
        return Response("Confirm callback", status=HTTP_200_OK)


class ValidateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        transaction = None
        try:
            source_ip = get_client_ip(request)
            transaction = TransactionLogBase().log_transaction(
                "ValidateData", request=request, source_ip=source_ip)
            # save the data
            request_data = get_request_data(request)
            # Perform your processing here e.g. print it out...
            print("validate data" + request_data)

            # Prepare the response, assuming no errors have occurred. Any response
            # other than a 0 (zero) for the 'ResultCode' during Validation only means
            # an error occurred and the transaction is cancelled
            message = {
                "ResultCode": 0,
                "ResultDesc": "The service was accepted successfully",
                "ThirdPartyTransID": "1234567890"
            }

            # Send the response back to the server
            TransactionLogBase().complete_transaction(
                transaction, response="100.000.000", description="Success")
            return Response(message, status=HTTP_200_OK)
        except Exception as ex:
            TransactionLogBase().mark_transaction_failed(
                transaction, response="999.999.999", description=str(ex))
            return JsonResponse({"code":"100.000.001"})
