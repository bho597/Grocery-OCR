from sqlalchemy.orm import Session
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from api.config.settings import GoogleSheetsSettings
from api.config import google_sheets

settings = GoogleSheetsSettings()


SPREADSHEET_ID = settings.spreadsheet_id
SHEET_NAME = settings.sheet_name

async def update_subtotal(db: Session, receipt):
    setattr(receipt, 'subtotal', round(receipt.total - receipt.total_tax, 2))
    db.commit()
    return True

def verify_total(receipt):
    return receipt.subtotal is not None and _float_equality(receipt.subtotal + receipt.total_tax - receipt.discount, receipt.total)
        
    
def verify_line_items(receipt, line_items):
    total = 0
    for line_item in line_items:
        if line_item.item_total_price:
            total += line_item.item_total_price
    return _float_equality(total, receipt.subtotal)

def _float_equality(float_1, float_2, tol=1e-3):
    return abs(float_1 - float_2) < tol

def read_google_sheet(range_name, spreadsheet_id=SPREADSHEET_ID):
    try:
        creds = google_sheets.get_credentials()
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        return values
    except HttpError as err:
        print(err)
        return None
    

def get_sheet_id(service, spreadsheet_id, sheet_name):
    # Get the specific sheetId by name
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in spreadsheet['sheets']:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']
    return None


def clear_google_sheet(service, range_name, spreadsheet_id=SPREADSHEET_ID, sheet_name=SHEET_NAME):
    # Get the specific sheetId by name
    sheet_id = get_sheet_id(service, spreadsheet_id, sheet_name)
    
    sheet = service.spreadsheets()
    clear_values_request = sheet.values().clear(spreadsheetId=spreadsheet_id, range=range_name)
    clear_values_response = clear_values_request.execute()
    
    # Clear the data validations (dropdowns)
    clear_data_validation_request = {
        "requests": [
            {
                "setDataValidation": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1000,  # Adjust according to the range you want to clear
                        "startColumnIndex": 0,
                        "endColumnIndex": 26  # Adjust according to the range you want to clear
                    }
                }
            }
        ]
    }
    
    batch_update_request = sheet.batchUpdate(spreadsheetId=spreadsheet_id, body=clear_data_validation_request)
    batch_update_response = batch_update_request.execute()
    
    return {
        "clear_values_response": clear_values_response,
        "clear_data_validation_response": batch_update_response
    }

def update_google_sheet(service, spreadsheet_id, range_name, values):
    body = {"values": values}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

    return result.get('updatedCells')


def apply_dropdown_to_column(service, spreadsheet_id, line_index_count, options):
    # Define the data validation rule
    rule = {
        "range": {
            "sheetId": 0,  # Replace with your actual sheet ID
            "startRowIndex": 1,  # Starting after the header
            "endRowIndex": line_index_count,  # Adjust for the number of rows
            "startColumnIndex": 3,  # Assuming 'bought_by' is the 3rd column (index 2)
            "endColumnIndex": 4
        },
        "rule": {
            "condition": {
                "type": "ONE_OF_LIST",
                "values": [{"userEnteredValue": str(option)} for option in options]
            },
            "strict": True,
            "showCustomUi": True
        }
    }

    # Apply the data validation rule using the Sheets API
    body = {
        "requests": [
            {
                "setDataValidation": {
                    "range": rule['range'],
                    "rule": rule['rule']
                }
            }
        ]
    }

    response = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body
    ).execute()

    return response

async def export_receipt_to_google_sheets(data, options, range_name='Sheet1!A1:Z1000'):
    creds = google_sheets.get_credentials()
    try:
        service = build("sheets", "v4", credentials=creds)
        clear_google_sheet(service, range_name="Sheet1")

        update_google_sheet(service, SPREADSHEET_ID, range_name, data)
        apply_dropdown_to_column(service, SPREADSHEET_ID, line_index_count=len(data), options=options)
    except HttpError as err:
        raise str(err)
