import pandas as pd

tempDict = {
        "ano": [],
        "numero_acidentes": []
    }

def addAnoToDf(ano, dfAcidentes):
    tempDict['ano'].append(ano)
    tempDict['numero_acidentes'].append(len(dfAcidentes))

acidentesBrasil2017 = pd.read_csv('./acidentes2017_todas_causas_tipos.csv', encoding="ISO-8859-9", sep=';')
acidentesBrasil2018 = pd.read_csv('./acidentes2018_todas_causas_tipos.csv', encoding="ISO-8859-9", sep=';')
acidentesBrasil2019 = pd.read_csv('./acidentes2019_todas_causas_tipos.csv', encoding="ISO-8859-9", sep=';')
acidentesBrasil2020 = pd.read_csv('./acidentes2020_todas_causas_tipos.csv', encoding="ISO-8859-9", sep=';')
acidentesBrasil2021 = pd.read_csv('./acidentes2021_todas_causas_tipos.csv', encoding="ISO-8859-9", sep=';')

acidentesRN2017 = acidentesBrasil2017.query("uf == 'RN'")
acidentesRN2018 = acidentesBrasil2018.query("uf == 'RN'")
acidentesRN2019 = acidentesBrasil2019.query("uf == 'RN'")
acidentesRN2020 = acidentesBrasil2020.query("uf == 'RN'")
acidentesRN2021 = acidentesBrasil2021.query("uf == 'RN'")

acidentesRN2017['ano'] = '2017'

print(len(acidentesRN2017))
print(len(acidentesRN2018))
print(len(acidentesRN2019))
print(len(acidentesRN2020))
print(len(acidentesRN2021))

addAnoToDf('2017', acidentesRN2017)
addAnoToDf('2018', acidentesRN2018)
addAnoToDf('2019', acidentesRN2019)
addAnoToDf('2020', acidentesRN2020)
addAnoToDf('2021', acidentesRN2021)

df = pd.DataFrame.from_dict(tempDict)

print(df)