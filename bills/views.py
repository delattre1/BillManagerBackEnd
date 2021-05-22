from django.shortcuts import render
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from .models import Bill
from .serializers import BillSerializer

import pdftotext
import requests

from .process_boleto import load_pdf, dados_boleto


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(['GET', 'POST'])
def api_bills(request):
    if request.method == 'POST':
        print(request.data)
        data = request.data
        data['vencimento'] = datetime.strptime(
            data['vencimento'], "%d/%m/%Y").strftime('%Y-%m-%d')
        new_bill = Bill(vencimento=data['vencimento'], empresa=data['empresa'],
                        valor=data['valor'], codigoPagamento=data['codigoPagamento'])
        new_bill.save()

    all_bills = Bill.objects.all()
    serialized_bill = BillSerializer(all_bills, many=True)

    return Response(serialized_bill.data)


@api_view(['GET', 'POST', 'DELETE'])
def api_bill(request, bill_id):
    if request.method == 'DELETE':
        bill = Bill.objects.get(id=bill_id)
        bill.delete()

    all_bills = Bill.objects.all()
    serialized_bill = BillSerializer(all_bills, many=True)

    return Response(serialized_bill.data)


@api_view(['GET', 'POST'])
def api_boleto(request):
    if request.method == 'POST':
        my_file = (request.data['File'])
        palavras = load_pdf(my_file)
        print(palavras)
        vencimento, valor, codigo_pagamento = dados_boleto(palavras)
        vencimento = datetime.strptime(
            vencimento, "%d/%m/%Y").strftime('%Y-%m-%d')
        empresa = 'Verificar'
        new_bill = Bill(vencimento=vencimento, empresa=empresa,
                        valor=valor, codigoPagamento=codigo_pagamento)
        new_bill.save()
        print(
            f'vencimento: {vencimento}, R$: {valor}, codigo: {codigo_pagamento}')

    return HttpResponse("Hello, world. You're at the polls index.")
