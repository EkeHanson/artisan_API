from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EscrowTransaction
from .serializers import EscrowTransactionSerializer, CreateEscrowTransactionSerializer


class EscrowTransactionListCreateView(APIView):
    def get(self, request):
        transactions = EscrowTransaction.objects.all()
        serializer = EscrowTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateEscrowTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = serializer.create_transaction(serializer.validated_data)
                return Response(EscrowTransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
