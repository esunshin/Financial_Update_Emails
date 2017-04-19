#main.py

from writer import *
import sys

def main():
    
    if(len(sys.argv) != 5):
        print("Usage: mailer.py <ticker file> <open time> <close time> <loop y/n>")
        exit(0)

    tickerFile = sys.argv[1]

    triggerOpenTime = sys.argv[2] 
    trigOpenHr,trigOpenMin = map(int, triggerOpenTime.split(':',1))

    triggerCloseTime = sys.argv[3]
    trigCloseHr,trigCloseMin = map(int, triggerCloseTime.split(':',1))
    
    trigOpen = (trigOpenHr, trigOpenMin);
    trigClose = (trigCloseHr, trigCloseMin);

    loopText = sys.argv[4][0:1].lower()
    loop = True if (loopText == "1" or loopText == "y") else False
    
    print("tickers = " + tickerFile)
    print("OTime   = " + str(trigOpen[0]) + ":" + str(trigOpen[1]))
    print("CTime   = " + str(trigClose[0]) + ":" + str(trigClose[1]))
    print("loop?   = " + str(loop))
    print("nowTime = " + str(getHMinCombo())) 
    writer = Write(tickerFile)

    if not loop:
        writer.updateAll()
        writer.writeAllPricesToFile("O")
        writer.writeFile('web.html')
        emailFile('web.html', 'addresses.txt')
        exit()

    while True:
        if isWeekday():
            if isTime(trigOpen):
                writer.updateAll()
                writer.writeAllPricesToFile("O")
                writer.writeFile('web.html')
                emailFile('web.html', 'addresses.txt')
            else:
                time.sleep(60)
        elif isTime(trigClose):
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
    return (datetime.now().hour, datetime.now().minute);

def isTime(theTime):
    curHr  = getHMinCombo()[0]
    curMin = getHMinCombo()[1]
    hrSame = (theTime[0] == currHr)
    minSame = (curMin in range(theTime[0], theTime[0] + 3))
    return (hrSame and minSame)

def isWeekday():
    day = datetime.now().weekday()
    return (day != 5 and day != 6)

if __name__ == "__main__":
    main()
