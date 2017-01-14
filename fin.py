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


class Finance:

    def __init__(self, finFile):
        self.news = {}
        self.prices = {}
        self.tickers = {}
        with open(finFile, "rb") as f:
            while True:
                textLine = f.readline()
                if not textLine: break
                splitLine = textLine.split(',',1)
                ticker = splitLine[0]
                nameN = splitLine[1]
                name = nameN.split('\n',1)[0]
                self.tickers[ticker] = name
        ticks = self.getCodes(self.tickers)

        for tick in ticks:
            news = self.getNewsForTicker(tick)
            self.news[tick] = news
            price = self.getPriceForTicker(tick)
            self.prices[tick] = price

    def updateAll(self):
        connected = self.internet_on()
        if(connected):
            self.updatePrices()
            self.updateNews()
        return connected
            
    def updatePrices(self):
        for tick in self.prices.keys():
            self.prices[tick] = self.getPriceForTicker(tick)

    def updateNews(self):
        for tick in self.news.keys():
            self.news[tick] = self.getNewsForTicker(tick)

    def getPriceForTicker(self, ticker):
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
        return price

    def getNewsForTicker(self, ticker):
        page = '0'
        while(page == '0'):
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, 'https://www.bloomberg.com/quote/' + ticker)
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue()
            page = body.decode('iso-8859-1')
        
        if(ticker == "SPX:IND"):
            d = page.split("companyNews",1)[1]
        else:
            d = page.split("newsBy",1)[1]
        data = d.split("[",1)[1]
        arts = data.split("headline",4)[1:4]
        
        Articles = [["" for x in range(2)] for y in range(3)]
        for i in range (0,3):
            j = 0
            Articles[i][0] = (arts[i].split("publishedAt",1)[0])[3:-3]
            if(ticker == "SPX:IND"):
                Articles[i][1] = ((arts[i].split("url",1)[1]).split("primaryCategory",1)[0])[3:-3]
            else:
                Articles[i][1] = ((arts[i].split("url",1)[1]).split("publishedAtISO",1)[0])[3:-3]
        return(Articles)

    def getCloseForTicker(self, ticker):
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
        return price

    def writeAllPricesToFile(self, OorC):
        for tick in self.tickers.keys():
            self.writePriceToFile(OorC, tick)

    def writePriceToFile(self, OorC, ticker):
        date = self.getDate()
        price = self.getPriceForTicker(ticker)
        target = OorC + ticker + ".csv"        
        line = ([OorC] + [price] + [date])
        with open(target, "a") as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(line)

    def getChange(self, ticker):
        currP = self.getPriceForTicker(ticker)
        origP = self.getCloseForTicker(ticker)
        cP = float(currP)
        oP = float(origP)
        diff = (cP - oP)
        change = (diff / oP) * 100
        return ('%.2f' % change)

    def getDate(self):
        day = str(datetime.now().day)
        month = str(datetime.now().month)
        year = str(datetime.now().year)
        date = month + "/" + day + "/" + year
        return date

    def getCodes(self, dict):
        codes = list(dict.keys())
        return codes

    def internet_on(self):
        try:
            response=urllib2.urlopen('https://www.google.com/',timeout=1)
            print("Connected to Internet")
            return True
        except urllib2.URLError as err:
            print("NOT Connected to Internet")
            return False


#def getPriceFromFile(ticker):
#    file = 'O' + ticker + ".csv"
#    with open(file, "rb") as f:
#        first = f.readline()
#        f.seek(-2, 2)
#        while f.read(1) != b"\n":
#            f.seek(-2, 1)
#        last = f.readline()
#
#        last1 = last.decode("utf-8")
#        price1 = last1.split(',', 2)[1]
#        price = price1.split("\r", 1)[0]
#    return price
