import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep


# Agregar informacion al archivo de google drive
def actualizar_valor(archivo, datos):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('Archivos/Ganaderia-360ba9db8bbe.json', scope)
    # authorize the clientsheet
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet_archivo = client.open(archivo)
    # get the first sheet of the Spreadsheet
    sheet_archivo_instance = sheet_archivo.get_worksheet(0)
    fila = sheet_archivo_instance.row_count
    sheet_archivo_instance.insert_row(values = list(datos.values()), index = fila)
    sleep(1)
