import zipfile
import urllib.request
import shutil

url = "https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip"  # noqa
file_name = "myzip.zip"

with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
    shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile(file_name) as zf:
        zf.extractall()
