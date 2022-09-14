from time import sleep
from flask import request
from flask import Response
import requests
from datetime import datetime, timedelta
from bot.variables import TOKEN, HOST_URL
from bot.H1Reports import h1Reports
from bot import app
from bot import db
from bot import scheduler
from flask import jsonify
from bot.models import DuplicateReport

requests.get(f'https://api.telegram.org/bot{TOKEN}/setWebhook?remove')
requests.get(f'https://api.telegram.org/bot{TOKEN}/setWebhook?url={HOST_URL}')

def healthRequest():
    r = requests.get(f'{HOST_URL}/healthcheck')
    return r 

scheduler.add_job(id="HealthCheck", func=healthRequest, trigger='interval', seconds=12000)

def parse_message(message):
    chat_id = message['message']['chat']['id']
    command = message['message']['text']
    print(f'message--> {message}')
    return chat_id,command

def tel_send_message(chat_id,payload):
    URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': payload,
        'parse_mode':'HTML'

    }

    r = requests.post(URL, json=payload)
    return r

def tel_send_photo(chat_id,photoURL,caption):

    URL = f'https://api.telegram.org/bot{TOKEN}/sendDocument'

    payload = {
        'chat_id': chat_id,
        'document': photoURL,
        'caption': caption,
        'parse_mode':'HTML'
    }

    r = requests.post(URL, json=payload)
    return r

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    status = {"status":"ok"}
    return jsonify(status)

@app.route('/', methods=['GET','POST'])
def index():

    if request.method == 'POST':
        msg = request.get_json()
        chat_id, command = parse_message(msg)

        try:
            if(command == '/start'):

                GreetingMsg = f"<b>Hello {msg['message']['from']['username']}! Glad to see you here!\n\rI'll be sending you reports of hacktivity from H1\n\rUse /help to see all capabilities.</b>"
                tel_send_message(chat_id, GreetingMsg)
            
            elif(command == '/update'):

                H1Reports = h1Reports()
                DupReport = False
                isUpdated = False
                dbrecord = DuplicateReport.query.filter_by(chat_id=chat_id).first()
                
                if not dbrecord:
                    newUser = DuplicateReport(chat_id=chat_id)
                    db.session.add(newUser)
                    db.session.commit()
                    dbrecord = DuplicateReport.query.filter_by(chat_id=chat_id).first()

                
                for report in reversed(H1Reports):

                    if not DupReport and not dbrecord.HackerOne_report_id:
                        DupReport = True
                        continue

                    elif (not DupReport and dbrecord.HackerOne_report_id == report['node']['id']):
                        DupReport = True
                        continue

                    elif DupReport:
                        reportTemplate = f"<b>\n\r\n\r{report['node']['report']['title']}\n\r</b><b>\n\r&#9889; {report['node']['report']['url']}\n\r</b><b>\n\r&#10071; Severity: {report['node']['severity_rating']}\n\r</b><b>&#128181; Bounty: {report['node']['total_awarded_amount']} {report['node']['currency']}\n\r</b><b>&#10062; Reported to: <a href=\"{report['node']['team']['url']}\">{report['node']['team']['name']}</a>\n\r</b><b>&#9937; Reported by: {report['node']['reporter']['username']}\n\r</b><b>&#8987; Disclosed at: {datetime.strptime(report['node']['latest_disclosable_activity_at'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%B %d %Y')}</b>"
                        tel_send_photo(chat_id, report['node']['team']['medium_profile_picture'], reportTemplate)
                        dbrecord.HackerOne_report_id = report['node']['id']
                        isUpdated = True
                        sleep(1)
                    
                    else:
                        continue
                
                if isUpdated:
                    db.session.commit()
                else:
                    Message = "<b>You're already up to date with H1 database!</b>"
                    tel_send_message(chat_id, Message)

            elif(command == '/leave'):

                dbrecord = DuplicateReport.query.filter_by(chat_id=chat_id).first()
                Message = f"<b>It was pleasure to work with you {msg['message']['from']['username']}! &#128546;\n\r\n\rAs you decided to leave the bot make the following actions:\n\r\n\r1. Open the bot menu and tap on 'Stop Bot' or 'Delete Chat' button.\n\r2. On your wish you can delete Chat with me by tapping on 'Clear messages' in the bot's menu.</b>"

                if dbrecord:
                    db.session.delete(dbrecord)
                    db.session.commit()

                tel_send_message(chat_id, Message)

            elif(command == '/help'):
                tel_send_message(chat_id, "<b>Use these commands to interact with the bot.\n\r/start - Use this command to start your bot.\n\r/update - Use this command to initiate an update process from H1 (It make take several seconds to run this command).\n\r/help - Use this command to display bot's possibility.</b>")

            else:
                tel_send_message(chat_id, "<b>Can't recognise this command.\n\rTry to use /help to view the allowed list of commands.</b>")
                
            return Response('ok', status=200)
        
        except Exception as e:
            print(e)
    
    else:
        return "<h1>Welcome!</h1>"