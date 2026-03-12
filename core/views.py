from django.http import JsonResponse
from django.shortcuts import render , get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Testing, Transaction, Budget
from core.serializers import TestingSerializer, TestingSerializer, TransactionSerializer, BudgetSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def testing_view(request):
    
    data = Testing.objects.all()
    serializer = TestingSerializer(data, many=True)

    return Response(serializer.data)
def health_check(request):
    return JsonResponse ({'status': 'OK'})

def testing_detail_view(request, id):
    test_data = get_object_or_404(Testing, id=id)
    serializer = TestingSerializer(test_data, many=True)
    return Response(serializer.test_data, safe=False)

class TransactionListView(APIView):
    """
    GET  /api/transactions/     -> List all transactions
    POST /api/transactions/     -> Create a new transaction
    """

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    """
    GET    /api/transactions/<id>/  -> Retrieve a single transaction
    PUT    /api/transactions/<id>/  -> Update a transaction
    DELETE /api/transactions/<id>/  -> Delete a transaction
    """

    def get_object(self, id):
        try:
            return Transaction.objects.get(id=id)
        except Transaction.DoesNotExist:
            return None

    def get(self, request, id):
        transaction = self.get_object(id)
        if transaction is None:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def put(self, request, id):
        transaction = self.get_object(id)
        if transaction is None:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        transaction = self.get_object(id)
        if transaction is None:
            return Response(
                {"error": "Transaction not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class BudgetListView(APIView):
    def get(self, request):
        budgets = Budget.objects.all()
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)