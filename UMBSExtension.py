# Created by Kenneth Thomas, Jr.
import time
import gspread
import requests
import webbrowser
from oauth2client.service_account import ServiceAccountCredentials

# Variable to easily change column data
nameOfSheet = 'GS1'
requestCol = 1
nameCol = 2
acctNumCol = 3
recieptCol = 4
addressCol = 5
phoneNoCol = 6
sourceCol = 7
amountCol = 8
linkCol = 9

# URLs for the UMBS API
# Extension
requestExtension = "https://umbstest.shreveportla.gov/UMBSTest/api/v1/RequestPaymentExtension/0E-C8-42-9A-73-A8-5C-B2-D5-13-B9-C1-F6-E8-5C-06/?AccountId=105650306"
checkEligibility = "https://umbstest.shreveportla.gov/UMBSTest/api/v1/IsPaymentExtensionEligible/0E-C8-42-9A-73-A8-5C-B2-D5-13-B9-C1-F6-E8-5C-06/?AccountId=105650306"
addToQueue = "https://umbstest.shreveportla.gov/UMBSTest/api/v1/PaymentExtensionToQueue/0E-C8-42-9A-73-A8-5C-B2-D5-13-B9-C1-F6-E8-5C-06/"

# Payment


# Function to gather data from sheets
def gatherSheets():
    # Authorization to access google sheets
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(nameOfSheet).sheet1

    length = len(sheet.get_all_records())

    # Assigning google sheet cells variables
    for i in range(length):
        x = i + 2
        request = sheet.cell(x, requestCol).value
        name = sheet.cell(x, nameCol).value
        accountId = sheet.cell(x, acctNumCol).value
        receipt = sheet.cell(x, recieptCol).value
        address = sheet.cell(x, addressCol).value
        phoneNum = sheet.cell(x, phoneNoCol).value
        source = sheet.cell(x, sourceCol).value
        amount = sheet.cell(x, amountCol).value
        link = sheet.cell(x, linkCol).value
        it = i
        print(i + 1, ") ", request, accountId, phoneNum, source, link)

        if request == 'Extension':
            handleExtension(it, request, name, accountId, address, link)
        elif request == 'Payment':
            handlePayment(it, request, name, accountId, receipt, address, phoneNum, source, amount, link)

        time.sleep(12)


# Function to handle Extension requests
def handleExtension(it, request, name, accountId, address, link):
    # Eligible Extension
    if requests.get(checkEligibility, accountId):
        note = ["SMS Type: ", request, "Name: ", name, "Address: ", address, "Extension Accepted"]

        print("Request Extension")
        print("Add To Queue")
        requests.get(requestExtension, accountId)
        requests.post(addToQueue, accountId, note)
        # webbrowser.open(link)  # Opens link to send confirmation text

    # Ineligible Extension
    elif not requests.get(checkEligibility, accountId):

        print("Request Denied")
        # webbrowser.open(link)  # Opens link to send confirmation text

def handlePayment(it, request, name, accountId, receipt, address, phoneNum, source, amount, link):
    print("Payment")

    note = [it, ")  ", "SMS Type: ", request, "Name: ", name, "Address: ", address, "Receipt No.: ", receipt, "Amount: ", amount, "Source: ", source, "Notification of Payment Received"]
    requests.post(addToQueue, accountId, note)
    # webbrowser.open(link)  # Opens link to send confirmation text


gatherSheets()
'''
notes = ["SMS Type: Payment", "Name: Kenneth Thomas", "Address: 123 ABC Rd.", "Receipt No.: 489646", "Amount: $11896", "Source: SMS", "Notification of Payment Received"]
url = "https://umbstest.shreveportla.gov/UMBSTest/api/v1/PaymentExtensionToQueue/0E-C8-42-9A-73-A8-5C-B2-D5-13-B9-C1-F6-E8-5C-06/"
accId = "100004304"
requests.post(url, accId, notes)
print("POSTED")
'''
