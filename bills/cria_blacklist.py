import json
import pdftotext
import re
from django.conf import settings


def remove_ponctuation(text):
    punctuation = '[!-.:?;@/…|_="\d+]'
    pattern = re.compile(punctuation)
    text_subbed = re.sub(pattern, '', text)

    return text_subbed


def get_name(palavras, blacklist):
    cleaned_words = [(remove_ponctuation(i)) for i in palavras if i.isupper()]
    empresa_possibilities = [
        word for word in cleaned_words if word not in blacklist]
    sem_duplicados = list(dict.fromkeys(empresa_possibilities))
    contador = 0
    index = 0
    nome_empresa = []

    while contador < 3:
        palavra = sem_duplicados[index]
        index += 1

        if len(palavra) > 2:
            contador += 1
        nome_empresa.append(palavra)

    return ' '.join(nome_empresa)


def load_pdf(path):
    with open(path, "rb") as f:
        pdf = pdftotext.PDF(f)
        pdf = pdf[0]

    split = pdf.split()
    clean = ' '.join(split).replace('_', '').replace(
        '-', '').replace('(', '').replace(')', '')  # .replace('/','')
    palavras = clean.split()

    return palavras


def get_words_isnt(path, empresa_words):
    palavras = load_pdf(path)
    cleaned_words = [(remove_ponctuation(i)) for i in palavras if i.isupper()]
    not_empresa = [word for word in cleaned_words if word not in empresa_words]

    return not_empresa


def get_array_blacklist():
    ex1 = '../media/ex1.pdf'
    ex2 = '../media/ex2.pdf'
    ex3 = '../media/ex3.pdf'
    ex4 = '../media/Boleto_0001_013688_144526.PDF'
    ex5 = '../media/bl204910p.pdf'

    dic_empresas = {ex1: ['CZECH', 'E', 'DAL', 'COL', 'ASSESSORIA', 'CONTÁBIL'],
                    ex2: ['MACPONTA', 'MAQUINAS', 'AGRICOLAS'],
                    ex3: ['AGROPARCERIA', 'MANUTENCAO', 'DE', 'MAQS', 'AGRICOLAS', 'LTDA'],
                    ex4: ['AM', 'COMERCIO', 'DE', 'MOLAS', 'LTDA'],
                    ex5: ['MACPONTA', 'MAQUINAS', 'AGRICOLAS'],
                    }

    words_isnt_empresa = []

    for path, empresa_words in dic_empresas.items():
        palavras_avulsas = get_words_isnt(path, empresa_words)
        words_isnt_empresa += palavras_avulsas

    return words_isnt_empresa


def save_file(array_words):
    data = {'words': array_words}
    with open('../media/blacklist.txt', 'w', encoding='utf-8') as file:
        json.dump(data, file)


def main():
    blacklist = get_array_blacklist()
    save_file(blacklist)


if __name__ == '__main__':
    main()
