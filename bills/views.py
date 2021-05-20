from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from .models import Bill
from .serializers import BillSerializer

import pdftotext
import requests
import PyPDF2
import io


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def load_pdf(pdf_file):
    pdf = pdftotext.PDF(pdf_file)
    pdf = pdf[0]

    split = pdf.split()
    clean = ' '.join(split).replace('_', '').replace(
        '-', '').replace('(', '').replace(')', '')  # .replace('/','')
    palavras = clean.split()

    return palavras


@api_view(['GET', 'POST'])
def api_bills(request):
    if request.method == 'POST':
        print(request.data)
        data = request.data
        new_bill = Bill(vencimento=data['vencimento'], empresa=data['empresa'],
                        valor=data['valor'], codigoPagamento=data['codigoPagamento'])
        new_bill.save()

    all_bills = Bill.objects.all()
    serialized_bill = BillSerializer(all_bills, many=True)

    return Response(serialized_bill.data)


@api_view(['GET', 'POST'])
def api_boleto(request):
    if request.method == 'POST':
        my_file = (request.data['File'])
        palavras = load_pdf(my_file)
        print(palavras)

    return HttpResponse("Hello, world. You're at the polls index.")
