#main.py

from fin import *

tickers = getTickers()
codes = getCodes(tickers)   #  list codes
for code in codes:
    print("Name: " + tickers[code]) #  print names
codes = getCodes(tickers)
triggerOpenTime = 930
triggerCloseTime = 1600
# while True:
#     if isWeekday():
#         if (isTime(triggerOpenTime)):
if(internet_on()):
    print("Connected to Internet")
    for ticker in codes:
        writePriceToFile("O", ticker, getDate())
    writeFile(tickers)
    time.sleep(10)
    print("Emailing file...")
    emailFile('web')
    print("Email sent")
    time.sleep(240)
else:
    print("NOT Connected to Internet")
#         elif (isTime(triggerCloseTime)):
if(internet_on()):
    print("Connected to Internet")
    for ticker in codes:
        writePriceToFile("C", ticker, getDate())
else:
    print("NOT Connected to Internet")


#         else:
#             time.sleep(60)
#     else:
#         time.sleep(3600)
