from datetime import datetime

screenToFind = "Prasads IMAX"
toEmailList = ["email_to_be_notified@gmail.com"] # Can be multiple email ids ["email1","email2","email3"]
fromEmail = "bms.from.email@gmail.com"
passwordOfFromEmail = "<Password>"


def notifyUser():
	openUrl()
	sendEmail(fromEmail, passwordOfFromEmail, toEmailList, screenToFind + ' Found!!', screenToFind + " is now listed. \nBook from here : "+url)

def openUrl():
	import webbrowser
	webbrowser.open(url)
	
def sendEmail(user, pwd, recipient, subject, body):
    import smtplib
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")


print("BMS Scrape started at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

import requests
url = "https://in.bookmyshow.com/buytickets/avengers-infinity-war-3d-hyderabad/movie-hyd-ET00053419-MT/"
request  = requests.get(url)
htmlContent = request.text

from bs4 import BeautifulSoup
soup = BeautifulSoup(htmlContent, "html.parser")
venueList = soup.find('ul', {'id': 'venuelist'})
found = False
availableList = ""
screenToFindLower = screenToFind.lower();
for link in venueList.find_all('li'):
    screenName = link.get('data-name')
    if(screenName.lower().find(screenToFindLower)>-1):
        found = True
        break
    availableList+=screenName + "\n"

if(found==False):
    print(screenToFind + ' not found')
else:
    print(screenToFind + " found! Triggering emails to: "+', '.join(emailList))
    notifyUser()
print("BMS Scrape completed at "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
