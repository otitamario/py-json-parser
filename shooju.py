import zipfile
import urllib.request
import shutil
import csv
import json


def get_csv_from_url(url, zip_file):
    with urllib.request.urlopen(url) as response, open(
        zip_file, "wb"
    ) as out_file:
        shutil.copyfileobj(response, out_file)
        with zipfile.ZipFile(zip_file) as zf:
            zf.extractall()


def process_csv_file(csv_filename):
    # abre o arquivo csv em modo leitura
    with open(csv_filename, "r") as csvfile:
        # cria um objeto de leitura csv
        csvreader = csv.reader(csvfile)

        # pula a primeira linha, que contém o cabeçalho
        headers = next(csvreader)

        # cria uma lista para armazenar as séries
        series_list = []

        # cria um dicionário para armazenar as séries
        series = {}

        # itera pelas linhas do arquivo csv
        for row in csvreader:
            # extrai o valor da coluna REF_AREA
            ref_area = row[0]

            # noqa se a série para esse valor ainda não foi criada, cria uma nova série vazia
            if ref_area not in series:
                series[ref_area] = []

            # noqa adiciona um novo dicionário para essa observação com as colunas e valores correspondentes
            observation = {}
            for i in range(1, len(headers)):
                observation[headers[i]] = row[i]
            series[ref_area].append(observation)

        # itera sobre as séries para gerar o JSON correspondente
        for ref_area in series:
            # cria um dicionário para a série
            serie_dict = {
                "ref_area": ref_area,
                "series_id": "series_" + ref_area,
                "fields": headers[1:],
                "values": series[ref_area],
            }
            series_list.append(serie_dict)

        # itera sobre as séries e as imprime no console
        for serie in series_list:
            print(json.dumps(serie, indent=4))

        # escreve todas as séries em um arquivo json
        with open("series.json", "w") as jsonfile:
            json.dump(series_list, jsonfile, indent=4)


if __name__ == "__main__":
    url = "https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip"  # noqa
    zip_file = "myzip.zip"
    get_csv_from_url(url, zip_file)
    filename = "jodi_gas_beta.csv"
    process_csv_file(filename)
