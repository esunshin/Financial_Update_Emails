#main.py

from writer import *
import sys

def main():
    tickerFile = sys.argv[1]
    triggerOpenTime = int(sys.argv[2])
    triggerCloseTime = int(sys.argv[3])
    loopText = sys.argv[4][0:1].lower()
    loop = True if (loopText == "1" or loopText == "y") else False
    
    print("tickers = " + tickerFile)
    print("OTime   = " + str(triggerOpenTime))
    print("CTime   = " + str(triggerCloseTime))
    print("loop?   = " + str(loop))
    
    writer = Write(tickerFile)

    if not loop:
        writer.updateAll()
        writer.writeAllPricesToFile("O")
        writer.writeFile('web.html')
        emailFile('web.html', 'addresses.txt')
        exit()

    while True:
        if isWeekday():
            if isTime(triggerOpenTime):
                writer.updateAll()
                writer.writeAllPricesToFile("O")
                writer.writeFile('web.html')
                emailFile('web.html', 'addresses.txt')
            else:
                time.sleep(60)
        elif isTime(triggerCloseTime):
            writer.updateAll()
            writer.writeAllPricesToFile("C")
        else:
            time.sleep(3600)

def test():
    print(type(getHMinCombo()))

def internet_on():
    try:
        response=urllib2.urlopen('https://www.google.com/',timeout=1)
        print("Connected to Internet")
        return True
    except urllib2.URLError as err: pass
    print("NOT Connected to Internet")
    return False

def emailFile(fileToEmail, addressFile):
    print("Emailing file...")
    email = getEmail(addressFile)
    yag = yagmail.SMTP(email[1], email[2])
    to = email[0]
    subject = 'Financial Update'
    body = (fileToEmail)
    yag.send(to = to, subject = subject, contents = body)
    print("Email sent")

def getEmail(addressFile):
    with open(addressFile, "rb") as f:
        email = f.readline()
    return email.split(',',2)

def getHMinCombo():
    return int(str(datetime.now().hour) + str(datetime.now().minute))

def isTime(theTime):
    return (getHMinCombo() in range(theTime, theTime + 3))

def isWeekday():
    day = datetime.now().weekday()
    return (day != 5 and day != 6)

if __name__ == "__main__":
    main()
