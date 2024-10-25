import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loadVars import load_settings
import json
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def getSheetData():
  
    sheet = getGoogleSheet()
    # Read tracking numbers and carriers from the Google Sheet
    data = sheet.get_all_records()

    # Adjusting column headers based on your sheet structure
    tracking_data = []
    status = ''
    for row in data:
        if row:
            if 'Status' in row:
                status = row["Status"].lower()
                if ('delivered' not in status):

                    # Keeping Tracking Number as string
                    trackingnum = row["Tracking"]  
                    carrier = '' #row["Carrier"]
                    tracking_data.append({"number": trackingnum, "carrier": carrier})
    
    
    #print("Request Payload:", json.dumps(tracking_data, indent=4))
    return tracking_data

def getSheetCarriers(numbers):
  
    sheet = getGoogleSheet()
    # Read tracking numbers and carriers from the Google Sheet
    data = sheet.get_all_records()

    # Adjusting column headers based on your sheet structure
    tracking_data = []
    if data:
        for row in data:
            if row:
                for num in numbers:
                    if (num == row["Tracking"].replace("\n", "")):
                        # Keeping Tracking Number as string
                        trackingnum = row["Tracking"]  
                        carrier = '' #row["Carrier"]
                        tracking_data.append({"number": trackingnum, "carrier": carrier})

    
    
    #print("Request Payload:", json.dumps(tracking_data, indent=4))
    return tracking_data

def updateSheetData(trackingdata):
    
    # Read tracking numbers and carriers from the Google Sheet
    sheet = getGoogleSheet()
    sheetdata = sheet.get_all_records()
    # Assuming you have logic to determine the shipping status based on the response
    row_index = 2
    
    for row in sheetdata:
        if row:
            print("Tracking NUmber from ExcelSheet Row: ",  row["Tracking"])
            for trackingrow in trackingdata:
                if trackingrow:
                    print("TrackingNumber from Response: ", trackingrow[0])
                    if row["Tracking"]:
                        if (row["Tracking"].replace("\n","") == trackingrow[0]):
                            # Update the Google Sheet with shipping statuses
                            sheet.update_cell(row_index, 3, trackingrow[11])  # Update column C with shipping status
                            sheet.update_cell(row_index, 9, trackingrow[2] + " " + trackingrow[3])  # Update column C with shipping status
                            sheet.update_cell(row_index, 10, trackingrow[10])  # Update column C with shipping status
                            """sheet.update_cell(row_index, 5, trackingrow[3])  # Update column C with shipping status
                            sheet.update_cell(row_index, 6, trackingrow[4])  # Update column C with shipping status
                            sheet.update_cell(row_index, 7, trackingrow[5])  # Update column C with shipping status
                            sheet.update_cell(row_index, 8, trackingrow[6])  # Update column C with shipping status
                            sheet.update_cell(row_index, 9, trackingrow[7])  # Update column C with shipping status
                            sheet.update_cell(row_index, 10, trackingrow[8])  # Update column C with shipping status"""
        row_index = row_index + 1
            

def getGoogleSheet():
    settings = load_settings()
    jsonkey_FileName = settings['jsonkey_FileName']
    google_ExcelFileName = settings['google_ExcelFileName']

    # print google variables
    #print(f'GoogleJsonFileLocation: {jsonkey_FileName}')
    #print(f'Excel File Name: {google_ExcelFileName}')
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(jsonkey_FileName, scope)
    client = gspread.authorize(creds)
    # Open the Google Sheet
    sheet = client.open(google_ExcelFileName).sheet1
    return sheet



