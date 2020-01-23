import gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, flash, redirect, render_template, request, session, make_response
from werkzeug.exceptions import default_exceptions
from tempfile import mkdtemp
import os
import json

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Pull in APIs stored as Heroku Config Vars and convert from multiline strings to JSON
client_secret = json.load('client_secret')

# scope = ['https://spreadsheets.google.com/feeds']
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)
# oauth2client.client.Credentials.refresh()
client = gspread.authorize(creds)

spreadsheet = client.open('WaynewoodReservations')
def worksheet(sheet):
    #client.login()
    return spreadsheet.worksheet(sheet)

lots = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '14', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', 'C']

rows_to_lots = {2: 'C', 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12, 14: 14, 15: 16, 16: 17, 17: 18, 18: 19, 19: 20, 20: 21, 21: 22, 22: 23, 23: 24, 24: 25, 25: 26, 26: 27, 27: 28, 28: 29, 29: 30, 30: 31, 31: 32, 32: 33, 33: 34, 34: 35, 35: 36, 36: 37, 37: 38, 38: 39, 39: 40, 40: 41, 41: 42, 42: 43, 43: 44, 44: 45, 45: 46, 46: 47, 47: 48, 48: 49, 49: 51, 50: 52, 51: 53, 52: 54, 53: 55, 54: 56, 55: 57, 56: 58, 57: 59, 58: 60}
lots_to_rows = {'C': 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 13, 14: 14, 16: 15, 17: 16, 18: 17, 19: 18, 20: 19, 21: 20, 22: 21, 23: 22, 24: 23, 25: 24, 26: 25, 27: 26, 28: 27, 29: 28, 30: 29, 31: 30, 32: 31, 33: 32, 34: 33, 35: 34, 36: 35, 37: 36, 38: 37, 39: 38, 40: 39, 41: 40, 42: 41, 43: 42, 44: 43, 45: 44, 46: 45, 47: 46, 48: 47, 49: 48, 51: 49, 52: 50, 53: 51, 54: 52, 55: 53, 56: 54, 57: 55, 58: 56, 59: 57, 60: 58}

def get_worksheet_titles(spreadsheet):
    #client.login()
    worksheet_list = spreadsheet.worksheets()
    worksheet_titles = []
    for worksheet in worksheet_list:
        title = str(worksheet).split('\'')
        worksheet_titles.append(title[1])
    return worksheet_titles


def make_reservation(event, lot, number):
    #client.login()
    l = lots_to_rows[lot]
    worksheet(event).update_cell(l,4, number)


@app.route("/", methods=["GET", "POST"])
def index():

    # print(request.form.get("lot"))

    if request.form.get("lot") == 'None':
        print("'None'")

    if request.form.get("lot") == None:
        print('None')

    if request.form.get("lot") == None:
        lot = None

    try:
        if lot is not None:
            pass
    except:
        lot = None

    # if 'lot' not in request.cookies:
    #             expire_date = datetime.datetime.now()
    #             expire_date = expire_date + datetime.timedelta(days=9000)
    #             resp.set_cookie('lot', str(lot), expires=expire_date)

    # resp = None

    # if request.form.get("lot") == None:
    #     print('Triggered Lot reset')
    #     resp.set_cookie('lot', None, expires = -1)
    
    try:
        print(f"lot is {lot} on line 67")
    except Exception:
        pass
        
    if lot != None and 'lot' not in locals():
        if 'lot' in request.cookies:
            lot = request.cookies.get('lot')
            if lot == 'C':
                pass
            else:
                lot = int(lot)
    
    try:
        print(f"lot is {lot} on line 77")
    except Exception:
        pass

    if request.method == "POST":
        # print('Triggered top if POST')

        if not request.form.get("event"):
            return apology("Please choose an event.", 400)

        try:
            number = request.form.get("number")
        except:
            pass
        try:
            number = request.form.get("num")
        except:
            pass
        if 'number' not in locals():
        # elif not request.form.get("number") or not request.form.get("num"):
            return apology("How many people are coming?", 400)

        elif not request.form.get("lot"):
            if not 'lot' in locals():
                return apology("Which lot are you RSVP'ing for?", 400)

        event = request.form.get("event")
        try:
            number = int(request.form.get("num"))
        except:
            number = int(request.form.get("number"))

        if lot is None or 'lot' not in locals():
            lot = int(request.form.get("lot"))

        try:
            print(event, lot, number)
        except:
            pass

        try:
            make_reservation(event, lot, number)
            reservation = True
                # f'Reservation is set to {reservation}'

        except:
            print('Entry didn\'t work.')

        if reservation == True:
            #client.login()
            resp = make_response(render_template("index.html", worksheet_titles=get_worksheet_titles(spreadsheet), lot=lot, event=event, number=number))
            if 'lot' not in request.cookies:
                expire_date = datetime.datetime.now()
                expire_date = expire_date + datetime.timedelta(days=9000)
                resp.set_cookie('lot', str(lot), expires=expire_date)
            return resp

    else:
        # print('Triggered bottom except')
        #client.login()
        return render_template("index.html", worksheet_titles=get_worksheet_titles(spreadsheet), lots = lots)

if __name__ == '__main__':
    app.run

