from rest_framework import serializers
from .models import Bill, Caixa


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'vencimento', 'empresa', 'valor', 'codigoPagamento']


class CaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caixa
        fields = ['id', 'data', 'valor', 'tipo']
