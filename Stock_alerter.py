import requests
import pandas as pd
import winsound
import time as time 
from datetime import datetime

from bs4 import BeautifulSoup

# webscraper for yahoo finance
def scrapeYahooPrice(url):    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    price = soup.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    price = price.replace(",", "")
    return float(price)


def alertBeep():
    winsound.Beep(2500,800)
    winsound.Beep(3000,500)    
    winsound.Beep(2500,800)
    winsound.Beep(3000,500)
    winsound.Beep(2500,800)


data = pd.read_csv("stock_watchlist.csv")

while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print("\nCurrent Time = ", current_time)

    for ndx in range(0, len(data) ):
        price = scrapeYahooPrice( data['Yahoo_URL'][ndx] )
        hi_thresh = float( data['Hi_thresh'][ndx] )
        lo_thresh = float( data['Lo_thresh'][ndx] )
        ticker = data['Ticker'][ndx]

        if price >= hi_thresh:
            print( "********** HI ALERT: " + ticker + " === " + str(price) + "   ABOVE thresh of " + str( hi_thresh ))
            alertBeep()
        elif price <= lo_thresh:
            print( "********** LO ALERT: " + ticker + " === " + str(price) + "   BELOW thresh of " + str( lo_thresh ))
            alertBeep()
        else:
            print( data['Ticker'][ndx] + " === " + str(price))

        time.sleep(8)   # pause 8 sec between successive tickers

    print('pausing for delay.......')
    time.sleep(900)    # pause 15 minutes between successive cycles
