#main.py

from fin import *

tickers = getTickers()
codes = getCodes(tickers)
triggerOpenTime = 930
triggerCloseTime = 1600
# while True:
#     if isWeekday():
#         if (isTime(triggerOpenTime)):

print(tickers)  #  print dictionary
codes = getCodes(tickers)   #  list codes
print(codes)    #  print codes
for code in codes:
    print("Name: " + tickers[code]) #  print names


if(internet_on()):
    print("Connected to Internet")
    for ticker in codes:
        writePriceToFile("O", ticker, getDate())
    writeFile(tickers)
    time.sleep(10)
    emailFile('web')
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

# getTo("addresses.txt")
# getFrom("addresses.txt")
# getPass("addresses.txt")


#         else:
#             time.sleep(60)
#     else:
#         time.sleep(3600)


# writePriceToFile("O", "GC1:COM", getDate())
# getChange("GC1:COM")