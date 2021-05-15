from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from .models import Bill
from .serializers import BillSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


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
