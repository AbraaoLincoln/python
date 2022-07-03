import pandas as pd

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

acidentesRnEntre2017E2021 = [acidentesRN2017, acidentesRN2018, acidentesRN2019, acidentesRN2020, acidentesRN2021]

ANO_2017 = 2017
FILTRO_MOTO_BIKE = "tipo_veiculo == 'Motocicleta' or tipo_veiculo == 'Motoneta' or tipo_veiculo == 'Bicicleta'"

def addNumeroAcidentesRn(ano, dfAcidentes, dic):
    dic['ano'].append(ano)
    dic['numero_acidentes'].append(len(dfAcidentes))

def getNumeroAcidentesRn():
    numeroAcidentesRnEntre2017e2021 = {
        "ano": [],
        "numero_acidentes": []
    }

    ano = ANO_2017
    for acidentesRn in acidentesRnEntre2017E2021:
        addNumeroAcidentesRn(ano, acidentesRn, numeroAcidentesRnEntre2017e2021)
        ano += 1
    return pd.DataFrame.from_dict(numeroAcidentesRnEntre2017e2021)

def getNumeroAcidentesRnMotoEBike():
    numeroAcidentesRnEntre2017e2021MotoEBike = {
        "ano": [],
        "numero_acidentes": []
    }

    ano = ANO_2017
    for acidentesRn in acidentesRnEntre2017E2021:
        acidentesRNMotoEBike = acidentesRn.query(FILTRO_MOTO_BIKE)
        addNumeroAcidentesRn(ano, acidentesRNMotoEBike, numeroAcidentesRnEntre2017e2021MotoEBike)
        ano += 1
    return pd.DataFrame.from_dict(numeroAcidentesRnEntre2017e2021MotoEBike)

numeroAcidentesRnEntre2017e2021 = getNumeroAcidentesRn()

print(numeroAcidentesRnEntre2017e2021)

numeroAcidentesRnEntre2017e2021MotoEBike = getNumeroAcidentesRnMotoEBike()

print(numeroAcidentesRnEntre2017e2021MotoEBike)

def showCausasAcidentesRnMotoEBike():
    ano = ANO_2017
    for acidentesRn in acidentesRnEntre2017E2021:
        print("============= ", ano, " =============")
        acidentesRNMotoEBike = acidentesRn.query(FILTRO_MOTO_BIKE)
        causaEquantidade = acidentesRNMotoEBike['causa_acidente'].value_counts()
        ano += 1
        print(causaEquantidade)

showCausasAcidentesRnMotoEBike()









