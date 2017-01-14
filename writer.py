# coding=iso-8859-1

from fin import *

class Write:

    def __init__(self, finFile):
        self.fence = Finance(finFile)
        self.tickers = self.fence.tickers
        self.prices = self.fence.prices
        self.news = self.fence.news

    def updateAll(self):
        return self.fence.updateAll()

    def printTicks(self):
        print(self.tickers)

    def writePrice(self, tick):
        price = self.prices[tick]
        writeText("    <a>$" + price + "</a><br>\n")

    def writeNews(self, tick):
        newsText = self.news[tick]
        style = "style=\"background-color:#E2E2E2;color:black;padding:5px;\""
        Articles = newsText
        web = ""
        for k in range (0,3):
            Articles[k][0] = Articles[k][0].translate({ord(c): None for c in 'â'})
            web = ("    <a href=\"" + Articles[k][1] + "\">" + Articles[k][0] + "</a>")
            writeText(web + "<br>" + "\n")

    def remFile(self, fileName):
        try:
            os.remove(fileName)
        except OSError as e:
            print("FILE DNE")

    def writeText(self, text, fileName):
        with open(fileName, 'a') as the_file:
            the_file.write(text)
        
    def writeTitle(self, title):
        writeText("    <b style=\"color:red\">" + title + "</b><br>\n")

    def writeLine(self, text):
        return (text + "\n")

    def writeFile(self, fileName):
        self.remFile(fileName)
        text = ""
        text += self.writeLine("<style>")
        text += self.writeLine("th, td {")
        text += self.writeLine("  padding: 5px")
        text += self.writeLine("}")
        text += self.writeLine("th {")
        text += self.writeLine("  text-align: left;")
        text += self.writeLine("}")
        text += self.writeLine("</style>")
        text += self.writeLine("<table style=\"width:50%\">")
        text += self.writeLine("  <tr>")
        text += self.writeLine("    <th>" + "Name" + "</th>")
        text += self.writeLine("    <th>" + "Current" + "</th>")
        text += self.writeLine("    <th>" + "Change" + "</th>")
        text += self.writeLine("  </tr>")

        for tick in self.tickers.keys():
            text += self.writeLine("  <tr>")
            text += self.writeLine(tick)
            text += self.writeLine("    <td>" + self.tickers[tick] + "</td>")
            text += self.writeLine("    <td>$" + self.prices[tick] + "</td>")
            change = self.fence.getChange(tick)
            if( float(change) > 0 ):
                text += self.writeLine("    <td style=\"color:#00A000\";>" + change + "%</td>")
            elif( float(change) < 0 ):
                text += self.writeLine("    <td style=\"color:#A00000\";>" + change + "%</td>")
            else:
                text += self.writeLine("    <td>" + change + "%</td>")
            text += self.writeLine("  </tr>")

        text += self.writeLine("</table>")
        print(text)
        self.writeText(text, fileName)

    def writeAllPricesToFile(self, OorC):
        self.fence.writeAllPricesToFile(OorC)

