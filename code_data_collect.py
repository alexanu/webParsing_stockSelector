#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np
import time

print('\n')
print('Software inizialised...Please wait...')
print('\n')
path = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html'

links_pages = list()
r = range(1,80)
for x in r:
    path = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/constituents-indices.html?&page=' + str(x)
    links_pages.append(path)



#fourWayKey collect
keys = list()

for link in links_pages:
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    soup = BeautifulSoup(webpage, 'html.parser')
    t = soup.select('a[title="View detailed prices page"]')
    for link_2 in t:
        link_2 = str(link_2)
        id = link_2[69:90]
        keys.append(id)
print(str(len(keys)) + ' companies found...')
print('\n')
print('Stocks keys obtained...')
print('\n')
print('Sleep...')
time.sleep(60)
print('Wake up...')
print('\n')

#Get main page link for each stocks
main_links = list()
for key in keys:
    stock_main_link = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary/' + key + '.html'
    main_links.append(stock_main_link)
print('Main page links for each stocks obtained...')
print('\n')


#Get fundamentals page link for each stocks
funda_links = list()
for key in keys:
    stock_funda_link = 'http://www.londonstockexchange.com/exchange/prices/stocks/summary/fundamentals.html?fourWayKey=' + key
    funda_links.append(stock_funda_link)
print('Fundamentals page links for each stocks obtained...')
print('\n')


#Get company name (from soup of key loop)
names = list()
count = 0
for link in main_links:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        name = str(soup.find("h1", class_="tesummary"))
        name = name.split('</a>')
        name = name[1].split('</')
        name = name[0].strip("\r\n")
        name = name.split("\r\n")
        name = name[0]
        names.append(name)
        count = count + 1
        print('company ' + str(count) + ' : done')
    except:
        count = count + 1
        name = np.nan
        names.append(name)
        print(link + ' : failed ' + 'index ' + str(main_links.index(link)))
print('Companies names obtained...')
print('\n')
print('Sleep...')
time.sleep(60)
print('Wake up...')
print('\n')


#Get currency
currency = list()
count = 0
for link in main_links:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        tbody = soup.find('tbody')
        c = tbody.find_all('td')
        c = str(c)
        c = c.split(', ')
        c = c[0]
        c = c.split('(')
        c = c[1].replace(")</td>", "")
        currency.append(c)
        count = count + 1
        print('company ' + str(count) + ' : done')
    except:
        count = count + 1
        c = np.nan
        currency.append(c)
        print(link + ' : failed ' + 'index ' + str(main_links.index(link)))
print('Share price currency obtained...')
print('\n')
print('Sleep...')
time.sleep(60)
print('Wake up...')
print('\n')

#Get current price share (from soup of key loop)
shares_prices = list()
count = 0
for link in main_links:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        tbody = soup.find('tbody')
        price = tbody.find_all('td')
        price = str(price)
        price = price.split(', ')
        price = price[1]
        price = price.replace("<td>", "")
        price = price.replace("</td>", "")
        price = price.replace(",", "")
        shares_prices.append(float(price))
        count = count + 1
        print('company ' + str(count) + ' : done')
    except:
        count = count + 1
        price = np.nan
        shares_prices.append(price)
        print(link + ' : failed ' + 'index ' + str(main_links.index(link)))
print('Companies current share price obtained...')
print('\n')
print('Sleep...')
time.sleep(60)
print('Wake up...')
print('\n')

#Get net asset value per share (pence)
companies_navps = list()
count = 0
for link in funda_links:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        x = str(soup.find_all("td", class_=""))
        x = x.split(', ')
        netAsset = x[-7]
        netAsset = netAsset.split('\n')
        netAsset = netAsset[1]
        if 'p' in netAsset:
            netAsset = netAsset.split('p')
            netAsset = netAsset[0]
        if '¢' in netAsset:
            netAsset = netAsset.split('¢')
            netAsset = netAsset[0]
        if '¥' in netAsset:
            netAsset = netAsset.split('¥')
            netAsset = netAsset[0]
        if 'c' in netAsset:
            netAsset = netAsset.split('c')
            netAsset = netAsset[0]
        netAsset = netAsset.rstrip()
        if ',' in netAsset:
            netAsset = netAsset.replace(",", "")
        companies_navps.append(float(netAsset))
        count = count + 1
        print('company ' + str(count) + ' : done')
    except:
        count = count + 1
        netAsset = np.nan
        companies_navps.append(netAsset)
        print(link + ' : failed ' + 'index ' + str(funda_links.index(link)))
print('Companies net asset value per share obtained...')
print('\n')
print('Sleep...')
time.sleep(60)
print('Wake up...')
print('\n')

#Getting Gearing % (from soup webpage fundamentals)
companies_gearing = list()
count = 0
for link in funda_links:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        x = str(soup.find_all("td", class_=""))
        x = x.split(', ')
        g = x[-1]
        g = g.split('\n')
        g = g[1]
        g = g.split('%')
        g = g[0]
        g = g.rstrip()
        if ',' in g:
            g = g.replace(",", "")
        companies_gearing.append(float(g))
        count = count + 1
        print('company ' + str(count) + ' : done')
    except:
        count = count + 1
        g = np.nan
        companies_gearing.append(g)
        print(link + ' : failed ' + 'index ' + str(funda_links.index(link)))
print('Companies gearings obtained...')
print('\n')
print('Sleep...')
time.sleep(60)
print('Wake up...')
print('\n')


#Get dividend yield
companies_yield = list()
count = 0
for link in funda_links:
    try:
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        soup = BeautifulSoup(webpage, 'html.parser')
        x = str(soup.find_all("td", class_=""))
        x = x.split(', ')
        div = x[-19]
        div = div.split('="">')
        div = div[1].split('<')
        div = div[0].strip('%')
        div = div.strip()
        if ',' in div:
            div = div.replace(",", "")
        companies_yield.append(float(div))
        count = count + 1
        print('company ' + str(count) + ' : done')
    except:
        count = count + 1
        div = np.nan
        companies_yield.append(div)
        print(link + ' : failed ' + 'index ' + str(funda_links.index(link)))
print('Companies dividend yields obtained...')
print('\n')


print('Building Data Frame...')
print('\n')
d = {'Currency': currency, 'Current Price per Share (pence)' : shares_prices, 'Net Asset Value per Share': companies_navps, 'Gearing (%)' : companies_gearing, 'Dividend Yield (%)' : companies_yield}
frame = pd.DataFrame(d, index=names)

frame.to_csv('original_table.csv')

print('Data Frame exported')
