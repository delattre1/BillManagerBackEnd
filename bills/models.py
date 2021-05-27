from django.db import models


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Bill(TimeStampMixin):
    vencimento = models.DateField()
    empresa = models.CharField(max_length=50)
    valor = models.FloatField()
    codigoPagamento = models.CharField(max_length=50)
    boleto = models.FileField(blank=True, null=True)

    def __str__():
        return f'{self.id} {self.empresa}'


class Caixa(TimeStampMixin):
    data = models.DateField()
    valor = models.FloatField()
    tipo = models.CharField(max_length=10)

    def __str__():
        return f'{self.id}'
