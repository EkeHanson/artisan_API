import requests  # Import the requests library
from rest_framework import serializers
from .models import EscrowTransaction
from users.models import CustomUser
from django.conf import settings


class EscrowTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowTransaction
        fields = ['id', 'buyer', 'seller', 'amount', 'description', 'status', 'escrow_id', 'created_at', 'updated_at']


class CreateEscrowTransactionSerializer(serializers.Serializer):
    buyer = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=500)

    def create_transaction(self, validated_data):
        buyer = validated_data['buyer']
        seller = validated_data['seller']
        amount = validated_data['amount']
        description = validated_data['description']

        # Call the escrow API
        response = requests.post(
            'https://api.escrow-sandbox.com/2017-09-01/transaction',
            auth=(settings.ESCROW_Email, settings.ESCROW_SANDBOX_SECRET_KEY),
            json={
                "parties": [
                    {"role": "buyer", "customer": buyer.email},
                    {"role": "seller", "customer": seller.email}
                ],
                "currency": "usd",
                "description": description,
                "items": [
                    {
                        "title": description,
                        "description": description,
                        "type": "service",
                        "quantity": 1,
                        "schedule": [
                            {"amount": float(amount), "payer_customer": buyer.email, "beneficiary_customer": seller.email}
                        ]
                    }
                ]
            }
        )

        if response.status_code == 200:
            data = response.json()
            escrow_id = data.get('id')
            return EscrowTransaction.objects.create(
                buyer=buyer, seller=seller, amount=amount, description=description, escrow_id=escrow_id
            )
        else:
            raise serializers.ValidationError("Failed to create escrow transaction")
