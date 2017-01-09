# coding=iso-8859-1

import string
import pycurl
import certifi
import csv
import os
import time
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
from datetime import datetime
import yagmail
import urllib2

def getNews(ticker):
    page = '0'
    while(page is None or page == '0'):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://www.bloomberg.com/quote/' + ticker)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        page = body.decode('iso-8859-1')
        d = page.split("newsBy",1)[1]
        data = d.split("[",1)[1]
        arts = data.split("headline",4)
    
        Articles = [["" for x in range(2)] for y in range(3)] 
        for i in range (1,4):
            j = 0
            Articles[i - 1][0] = (arts[i].split("publishedAt",1)[0])[3:-3]
            Articles[i - 1][1] = ((arts[i].split("url",1)[1]).split("publishedAtISO",1)[0])[3:-3]
        return(Articles)

def getPrice(ticker):
    price = 0
    while(price == 0):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(c.URL, 'https://www.bloomberg.com/quote/' + ticker)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        page = body.decode('iso-8859-1')
        data = page.split("lastPrice",1)[1]
        price = data.split("}",1)[0][2:]
        print(price)
    print(price)
    return price

def getClose(ticker):
    price = 0
    while(price == 0):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(c.URL, 'https://www.bloomberg.com/quote/' + ticker)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()
        page = body.decode('iso-8859-1')
        data = page.split("previousClosingPriceOneTradingDayAgo",1)[1]
        price = data.split(",",1)[0][2:]
        print(price)
    print(price)
    return price
    
def writeNews(news):
    style = "style=\"background-color:#E2E2E2;color:black;padding:5px;\""
    Articles = news    
    web = ""
    for k in range (0,3):
        Articles[k][0] = Articles[k][0].translate({ord(c): None for c in 'â'})
        web = ("    <a href=\"" + Articles[k][1] + "\">" + Articles[k][0] + "</a>")
        writeText(web + "<br>" + "\n")        

def writePrice(price):
    writeText("    <a>$" + price + "</a><br>\n")

def writeTitle(title):
    writeText("    <b style=\"color:red\">" + title + "</b><br>\n")

def remFile():
    try:
        os.remove('web.html')
    except OSError as e:
        print("FILE DNE")

def writeText(text):
    with open('web.html', 'a') as the_file:
        the_file.write(text)

def writeTextLine(text):
    return (text + "\n")

def writeFile(dict):
    tickers = getTickers()
    remFile()
    text = ""
    text += writeTextLine("<style>")
    text += writeTextLine("th, td {")
    text += writeTextLine("  padding: 5px")
    text += writeTextLine("}")
    text += writeTextLine("th {")
    text += writeTextLine("  text-align: left;")
    text += writeTextLine("}")
    text += writeTextLine("</style>")
    text += writeTextLine("<table style=\"width:50%\">")
    text += writeTextLine("  <tr>")
    text += writeTextLine("    <th>" + "Name" + "</th>")
    text += writeTextLine("    <th>" + "Current" + "</th>")
    text += writeTextLine("    <th>" + "Change" + "</th>")
    text += writeTextLine("  </tr>")

    for ticker in tickers: 
        text += writeTextLine("  <tr>")
        text += writeTextLine("    <td>" + getName(dict, ticker) + "</td>")
        text += writeTextLine("    <td>$" + getPrice(ticker) + "</td>")
        change = getChange(ticker)
        if( float(change) > 0 ):
            text += writeTextLine("    <td style=\"color:#00A000\";>" + change + "%</td>")           
        elif( float(change) < 0 ):
            text += writeTextLine("    <td style=\"color:#A00000\";>" + change + "%</td>")
        else:
            text += writeTextLine("    <td>" + getChange(ticker) + "%</td>")
        text += writeTextLine("  </tr>")

    text += writeTextLine("</table>")
    print(text)
    writeText(text)

def emailFile(fileName):
    yag = yagmail.SMTP('ezra.sunshine', 'ESunshine17')
    to = 'ezra.sunshine@gmail.com'
    subject = 'Financial Update'
    body = (fileName + '.html')
    yag.send(to = to, subject = subject, contents = body)

def writePriceToFile(OorC, ticker, date):
    price = getPrice(ticker)
    target = OorC + ticker + ".csv"        
    line = ([OorC] + [price] + [date])
    with open(target, "a") as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(line)

def getPriceFromFile(ticker):
    file = 'O' + ticker + ".csv"
    with open(file, "rb") as f:
        first = f.readline()
        f.seek(-2, 2)
        while f.read(1) != b"\n":
            f.seek(-2, 1)
        last = f.readline()

        last1 = last.decode("utf-8")
        price1 = last1.split(',', 2)[1]
        price = price1.split("\r", 1)[0]
    return price

def getChange(ticker):

    currP = getPrice(ticker)
    origP = getClose(ticker)
    cP = float(currP)
    oP = float(origP)
    diff = (cP - oP)
    change = (diff / oP) * 100
    print("differ " + str(diff))
    print("change " + str(change))
    return ('%.2f' % change)


    # currP = getPriceFromFile(ticker)
#     openP = getClose(ticker)
#     print("Curr: $" + currP)
#     print("Open: $" + openP)
    

def getDate():
    day = str(datetime.now().day)
    month = str(datetime.now().month)
    year = str(datetime.now().year)
    date = month + "/" + day + "/" + year
    print(date)
    return date
    
def getHMinCombo():
    return int(str(datetime.now().hour) + str(datetime.now().minute))
    
def isTime(theTime):
    return (getHMinCombo() in range(theTime, theTime + 3))

def isWeekday():
    day = datetime.now().weekday()
    return (day != 5 and day != 6)
    
def getTickers():
    tickers = {"CL1:COM": "Crude", 
            "GC1:COM": "Gold",
            "EURUSD:CUR": "Euro/Dollar", 
            "USGG10YR:IND": "10Yr Bond", 
            "SPX:IND": "S&P"}
    return tickers 

#   https://www.bloomberg.com/quote/GC1:COM

def getCodes(dict):
    codes = list(dict.keys())
    return codes

def getName(dict, code):
    return dict[code]
    
def internet_on():
    try:
        response=urllib2.urlopen('https://www.google.com/',timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

