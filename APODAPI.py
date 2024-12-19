import requests
import gspread
import webbrowser
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def apod(api_key):
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        print(f"You are Good to Go! {response.status_code} received ")
        return response.json()
    else:
        print("Access Denied")
        return None


def title(apod_data):
    return apod_data.get('title')


def author(apod_data):
    return apod_data.get('copyright')


def date(apod_data):
    return apod_data.get('date')


def explanation(apod_data):
    return apod_data.get('explanation')


def picture(apod_data):
    return apod_data.get('hdurl')


def apodAPI(apod_data):
    print(f'Title : {title(apod_data)}')
    print(f'Author : {author(apod_data)}')
    print(f'Date : {date(apod_data)}')
    print(f'Explanation : {explanation(apod_data)}')
    print(f'Picture of the Day : {picture(apod_data)}')



def spreadsheet(apod_data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('token.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('APOD').sheet1

    data = [
        title(apod_data),
        author(apod_data),
        date(apod_data),
        explanation(apod_data),
        ""
    ]

    sheet.append_row(data)
    last_row = len(sheet.get_all_values())

    image_formula = f'=IMAGE("{picture(apod_data)}", 1)'

    sheet.update_cell(last_row, 5, image_formula)

    print("Data successfully written to Google Sheets, including the image!")



def main():
    api_key = "BoDCXqe53cZ1DDHkzcjzMlqoZsvDxDPrrKWquyNf"
    apod_data = apod(api_key)
    if apod_data:
        apodAPI(apod_data)
        spreadsheet(apod_data)


if __name__ == "__main__":
    main()
