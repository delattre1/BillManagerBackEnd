import pdftotext
import re
from datetime import datetime
import os
from .cria_blacklist import get_name
import json


def load_pdf(pdf_file):
    pdf = pdftotext.PDF(pdf_file)
    pdf = pdf[0]

    split = pdf.split()
    clean = ' '.join(split).replace('_', '').replace(
        '-', '').replace('(', '').replace(')', '')  # .replace('/','')
    palavras = clean.split()

    return palavras


def is_float(val):
    val = val.replace(',', '.')

    return all([[any([i.isnumeric(), i in ['.', 'e']]) for i in val],  len(val.split('.')) == 2])


def is_float_or_int(string):
    try:
        int(string)

        return True
    except:
        try:
            return is_float(string)
        except:
            return False


def get_empresa(palavras, blacklist_path):
    blacklist = get_blacklist(blacklist_path)
    empresa = get_name(palavras, blacklist)

    return empresa


def get_blacklist(blacklist_path):
    with open(blacklist_path) as file:
        data = json.load(file)
        words = data['words']

        return words


def dados_boleto(palavras, blacklist_path):
    datas_vencimento = []
    valores_boleto = []
    codigo_de_barras = []
    possiveis_codigos = []

    for i in range(len(palavras) - 10):
        if palavras[i] == "Vencimento":
            for j in range(i, i+10):
                if data_valida(palavras[j]):
                    datas_vencimento.append(palavras[j])

        if palavras[i] == "Valor":
            for j in range(i, i+8):
                if is_float(palavras[j]):
                    valores_boleto.append(palavras[j])

        maybe_is_the_code = True

        for j in range(i, i+5):
            if not is_float_or_int(palavras[j]):
                maybe_is_the_code = False

                continue

        if maybe_is_the_code:
            possiveis_codigos.append(palavras[i:i+5])

    data_vencimento = validate_dados(datas_vencimento)
    valor = str(validate_dados(valores_boleto))
    valor = valor.replace(',', '.')
    codigo_pagamento = select_rigth_code_from_list(possiveis_codigos)
    empresa = get_empresa(palavras, blacklist_path)

    return data_vencimento, valor, codigo_pagamento, empresa


def data_valida(data):
    try:
        datetime.strptime(data, '%d/%m/%Y')

        return True
    except ValueError:
        return False


def validate_dados(lista):
    try:
        return max(set(lista), key=lista.count)
    except:
        return 1
        # return f"some error with {lista}"


def correct_bar_code(codigo):
    split = codigo.split()
    without_spaces = ('').join(split)
    tamanho_codigo = (len(without_spaces))

    if tamanho_codigo == 47 or tamanho_codigo == 48:
        return codigo

    elif tamanho_codigo > 48 and tamanho_codigo < 53:
        codigo_corrigido = (' '.join(split[1:]))

        return codigo_corrigido

    else:
        return False


def select_rigth_code_from_list(lista_possibilities):
    for i in lista_possibilities:
        code = ((' ').join(i).replace('.', ' '))
        codigo = correct_bar_code(code)

        if codigo is not False:
            return codigo
