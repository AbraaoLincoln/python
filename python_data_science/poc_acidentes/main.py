import pandas as pd

acidentesBrasil = pd.read_csv('./datatran2021.csv', encoding="ISO-8859-9", sep=';')

filterAcidentesRN = acidentesBrasil['uf'] == 'RN'
acidentesRN = acidentesBrasil.loc[filterAcidentesRN]

# acidentesRN.plot.bar(x='causa_acidente', y='feridos', figsize=(12,6))

# print(acidentesRN['causa_acidente'].value_counts())

causas_acidentes = acidentesRN['causa_acidente'].unique()
# print(causas_acidentes)


def generateDataFrameForCausaAcidenteAnd(x):
    tempDict = {
        "causa_acidente": [],
        x: []
    }

    for causa in causas_acidentes:
        filterCausaAcidente = acidentesRN['causa_acidente'] == causa
        acidenteComCausa = acidentesRN.loc[filterCausaAcidente]
        sumResult = acidenteComCausa[x].sum()
        tempDict['causa_acidente'].append(causa)
        tempDict[x].append(sumResult)
        print(causa + ": " + str(sumResult))

    df = pd.DataFrame.from_dict(tempDict)

    return df

print(generateDataFrameForCausaAcidenteAnd('feridos'))