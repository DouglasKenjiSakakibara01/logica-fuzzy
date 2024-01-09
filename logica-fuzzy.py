import random as rd
import pandas as pd

def trifp(x, a, b, c):
    return max(min((x - a) / (b - a), (c - x) / (c - b)), 0)

def lhalftrapfp(x, a, b):
    return 1 if x <= a else max((b - x) / (b - a), 0)
    
def rhalftrapfp(x, a, b):
    return 1 if x >= b else max((x - a) / (b - a), 0)

def trapfp(x, a, b, c, d):
    return max(min((x - a) / (b - a), 1, (d - x) / (d - c)), 0)

JOVEM = 0
MEIA_IDADE = 1
IDOSO = 2

def fps_idade(idade):
    return lhalftrapfp(idade, 25, 40), trapfp(idade, 27, 43, 47, 63), rhalftrapfp(idade, 50, 65)

DESEJAVEL = 0
LIMITROFE = 1
ALTO = 2
MUITO_ALTO = 3

def fps_colesterol(colesterol):
    return lhalftrapfp(colesterol, 180, 195), trifp(colesterol, 185, 195, 220), trapfp(colesterol, 205, 225, 250, 300), rhalftrapfp(colesterol, 280, 305)

PRESSAO_NORMAL = 0
PRE_HIPERTENSAO = 1
HIPERTENSAO_LEVE = 2
HIPERTENSAO_GRAVE = 3

def fps_pressao(pressao):
    return lhalftrapfp(pressao, 105, 135), trifp(pressao, 123, 130, 155), trifp(pressao, 135, 165, 195), rhalftrapfp(pressao, 166, 198)

BOA = 0
TAXA_NORMAL = 1
RUIM = 2

def fps_taxa(taxa):
    return lhalftrapfp(taxa, 150, 190), trapfp(taxa, 160, 190, 195, 210), rhalftrapfp(taxa, 200, 220)

BAIXA = 0
MEDIA = 1
ALTA = 2

def fps_doenca_cardiaca(prob):
    return lhalftrapfp(prob, 20, 45), trifp(prob, 25, 50, 75), rhalftrapfp(prob, 55, 75)

def inferencia_doenca_cardiaca(pert_idade, pert_colesterol, pert_pressao, pert_taxa):
    infere_alta = [
        # Se tem 2 sintomas graves
        min(pert_colesterol[MUITO_ALTO], pert_pressao[HIPERTENSAO_GRAVE]),
        # Se tem 1 sintoma grave e não é (jovem e tem pressão normal e tem taxa boa) - ou seja, tem apenas 1 sintoma grave e de resto é saudável
        min(pert_colesterol[MUITO_ALTO], 1 - min(pert_idade[JOVEM], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA])),
        min(pert_pressao[HIPERTENSAO_GRAVE], 1 - min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_taxa[BOA])),
        # Se é idoso, e tem (1 sintoma leve ou taxa ruim) e não tem (algum pré sintoma e taxa boa) ou (dois pré sintomas e taxa normal)
        min(pert_idade[IDOSO], max(min(pert_colesterol[ALTO], 1 - min(pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA])),
                                   min(pert_pressao[HIPERTENSAO_LEVE], 1 - min(pert_colesterol[DESEJAVEL], pert_taxa[BOA])),
                                   min(pert_taxa[RUIM], 1 - min(pert_pressao[PRESSAO_NORMAL], pert_colesterol[DESEJAVEL])),
                                   min(pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]))),
        # Se tem colesterol alto e tem (hipertensão leve ou taxa ruim) e não é (jovem e tem taxa boa ou pressão normal) ou (é de meia idade, com pre hipertensão e taxa normal)
        min(pert_colesterol[ALTO], max(min(pert_pressao[HIPERTENSAO_LEVE], 1 - min(pert_idade[JOVEM], pert_taxa[BOA])),
                                       min(pert_taxa[RUIM], 1 - min(pert_idade[JOVEM], pert_pressao[PRESSAO_NORMAL])),
                                       min(pert_idade[MEIA_IDADE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]))),
        # Se tem hipertensão leve e tem taxa ruim e não é (jovem e tem colesterol baixo) ou (é de meia idade, com colesterol limitrofe e taxa normal)
        min(pert_pressao[HIPERTENSAO_LEVE], max(pert_taxa[RUIM], 1 - min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL]),
                                                min(pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_taxa[TAXA_NORMAL]))),
        # Se tem taxa ruim, é de meia idade, tem 2 pré sintomas
        min(pert_taxa[RUIM], pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO])
    ]
    infere_media = [
        # Se tem um sintoma grave, mas é jovem e não tem outro pré-sintoma e tem taxa boa
        min(pert_colesterol[MUITO_ALTO], pert_idade[JOVEM], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_pressao[HIPERTENSAO_GRAVE], pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_taxa[BOA]),
        # Se é idoso e tem (um sintoma leve, mas não tem outro pré sintoma e tem taxa boa) ou tem (um pré sintoma ou taxa normal)
        min(pert_idade[IDOSO], max(min(pert_colesterol[ALTO], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
                                   min(pert_pressao[HIPERTENSAO_LEVE], pert_colesterol[DESEJAVEL], pert_taxa[BOA]),
                                   min(pert_taxa[RUIM], pert_pressao[PRESSAO_NORMAL], pert_colesterol[DESEJAVEL]))),
        # Se tem colesterol alto e ou (tem hipertensao leve, mas é jovem e tem taxa boa) ou (tem taxa ruim, mas é jovem e tem pressão normal)
        min(pert_colesterol[ALTO], max(min(pert_pressao[HIPERTENSAO_LEVE], pert_idade[JOVEM], pert_taxa[BOA]),
                                       min(pert_taxa[RUIM], pert_idade[JOVEM], pert_pressao[PRESSAO_NORMAL]))),
        # Se tem hipertensão leve e taxa ruim, mas é jovem e tem colesterol desejavel)
        min(pert_pressao[HIPERTENSAO_LEVE], pert_taxa[RUIM], pert_idade[JOVEM], pert_colesterol[DESEJAVEL]),
        # Se é de meia idade e tem 2 pré sintomas ou taxa normal
        min(pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[MEIA_IDADE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]),
        # Se tem 2 pré sintomas e taxa normal
        min(pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]),
        # Se é idoso e tem 2 pré sintomas e/ou 1 pré sintoma e taxa normal
        min(pert_idade[IDOSO], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_idade[IDOSO], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[BOA]),
        min(pert_idade[IDOSO], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[IDOSO], pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[BOA]),
        min(pert_idade[IDOSO], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[IDOSO], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]),
        # Se tem colesterol alto e é de meia idade e tem taxa normal ou pré hipertensão, e/ou é jovem mas tem taxa normal e pré hipertensao
        min(pert_idade[MEIA_IDADE], pert_colesterol[ALTO], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[ALTO], pert_pressao[PRE_HIPERTENSAO], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[ALTO], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[ALTO], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[ALTO], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[JOVEM], pert_colesterol[ALTO], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]),
        # Se tem hipertensao leve e é de meia idade e tem colesterol limitrofe ou taxa normal, ou é jovem mas tem taxa normal e colesterol limitrofe
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[HIPERTENSAO_LEVE], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[HIPERTENSAO_LEVE], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_pressao[HIPERTENSAO_LEVE], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_pressao[HIPERTENSAO_LEVE], pert_taxa[BOA]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[HIPERTENSAO_LEVE], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[HIPERTENSAO_LEVE], pert_taxa[TAXA_NORMAL]),
        # Se tem taxa ruim e é de meia idade e tem um pré sintoma, e/ou 2 pré sintomas
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL], pert_taxa[RUIM]),
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[RUIM]),
        min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[RUIM]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[RUIM]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[RUIM]),
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[RUIM])
    ]
    infere_baixa = [
        # Se tem um sintoma leve ou é idoso ou tem taxa ruim, mas de resto está saudavel
        min(pert_idade[IDOSO], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_colesterol[ALTO], pert_idade[JOVEM], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_pressao[HIPERTENSAO_LEVE], pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_taxa[BOA]),
        min(pert_taxa[RUIM], pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL]),
        # Se tem um pré sintoma ou é de meia idade ou tem taxa normal, mas de resto está saudável
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        # Se é de meia idade e tem um pré sintoma ou taxa normal
        min(pert_idade[MEIA_IDADE], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[BOA]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[BOA]),
        min(pert_idade[MEIA_IDADE], pert_colesterol[DESEJAVEL], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        # Se tem dois pré sintomas ou um pré sintoma e taxa normal
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[PRE_HIPERTENSAO], pert_taxa[BOA]),
        min(pert_idade[JOVEM], pert_colesterol[LIMITROFE], pert_pressao[PRESSAO_NORMAL], pert_taxa[TAXA_NORMAL]),
        min(pert_idade[JOVEM], pert_colesterol[DESEJAVEL], pert_pressao[PRE_HIPERTENSAO], pert_taxa[TAXA_NORMAL]),
    ]

    return (max(infere_baixa), max(infere_media), max(infere_alta))

def defuzz(pert_doenca):
    result = 0
    ponder = 0
    if pert_doenca[BAIXA] > 0:
        result += (10 + 20) * pert_doenca[BAIXA]
        ponder += 2 * pert_doenca[BAIXA]
        if pert_doenca[MEDIA] == 0:
            result += (30 + 40 + 50) * pert_doenca[BAIXA]
            ponder += 3 * pert_doenca[BAIXA]
    if pert_doenca[MEDIA] > 0:
        result += (30 + 40 + 50) * pert_doenca[MEDIA]
        ponder += 3 * pert_doenca[MEDIA]
        if pert_doenca[ALTA] == 0:
            result += (60 + 70) * pert_doenca[MEDIA]
            ponder += 2 * pert_doenca[MEDIA]
    if pert_doenca[ALTA] > 0:
        result += (60 + 70 + 80 + 90 + 100) * pert_doenca[ALTA]
        ponder += 5 * pert_doenca[ALTA]
    return result / ponder

idade = 38
colesterol = 127
pressao = 174
taxa = 67
pert_doenca = inferencia_doenca_cardiaca(fps_idade(idade), fps_colesterol(colesterol), fps_pressao(pressao), fps_taxa(taxa))
print(f'Resultado inferência (fuzzy): {pert_doenca}')
print(f'Resultado inferência (crisp): {defuzz(pert_doenca)}')

dataset = pd.read_csv('./heart.csv')
dataset = dataset[['age', 'chol', 'trtbps', 'thalachh', 'output']]

dataset['pert_idade'] = dataset.apply(lambda x: fps_idade(x['age']), axis=1)
dataset['pert_colesterol'] = dataset.apply(lambda x: fps_colesterol(x['chol']), axis=1)
dataset['pert_pressao'] = dataset.apply(lambda x: fps_pressao(x['trtbps']), axis=1)
dataset['pert_taxa'] = dataset.apply(lambda x: fps_taxa(x['thalachh']), axis=1)

dataset['pert_doenca'] = dataset.apply(lambda x: inferencia_doenca_cardiaca(x['pert_idade'], x['pert_colesterol'], x['pert_pressao'], x['pert_taxa']), axis=1)

dataset['resultado'] = dataset.apply(lambda x: defuzz(x['pert_doenca']), axis=1)

dataset['acerto'] = dataset.apply(lambda x: rd.random() < x['resultado'] / 100, axis=1)

total = 0

for i in range(10):
    dataset['acerto'] = dataset.apply(lambda x: rd.random() < x['resultado'] / 100, axis=1)
    total += dataset['acerto'].values.sum()/len(dataset.index)

print(total / 10)
