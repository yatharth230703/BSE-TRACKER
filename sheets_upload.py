import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os 
def sheets_updater(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    script_dir=os.path.dirname(os.path.abspath(__file__))
    fileloc= os.path.join(script_dir, "bse-updater-project-5994bba9d344.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(fileloc, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/191406Q_-pdf4zXTKJRrvOhr7W_UXn-bU9KrQ2OncDNk/edit?usp=sharing')

    worksheet = sheet.get_worksheet(0)  

    worksheet.append_row(data)

    print("data_uploaded")
    
