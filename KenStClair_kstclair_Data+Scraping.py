
# coding: utf-8

# In[128]:


#Send get request to website
# import libraries
import requests
from bs4 import BeautifulSoup
import time
from dateutil.parser import parse

months = []
ios = []
android = []

for year in range(2007, 2018):
    quote_page = 'https://www.netmarketshare.com/operating-system-market-share.aspx?qprid=9&qpcustomb=1&qpsp=%d&qpnp=1&qptimeframe=Y' % (year)
    r = requests.get(quote_page)

    #Parse response text using BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    #get the table by id
    table = soup.find('table', attrs={'id': 'fwReportTable1'})

    #pull tr's with class rpt-row or rpt-row2
    def report_rows(tag):
        #print(tag.attrs)
        return (tag.name == 'tr' and (tag['class']==['rpt-row']
                or tag['class']==['rpt-row2']))
    rows = table.findAll(report_rows)

    #grab the corresponding columns
    for row in rows:
        cols = row.findAll('td')
        months.append(parse(cols[0].text)) 
        ios.append(float(cols[1].text[:-1])) #remove % from end
        android.append(float(cols[2].text[:-1]))# remove % from end
        print ('month: ' + cols[0].text + ' ios: ' + cols[1].text + ' android: ' + cols[2].text)

    time.sleep(1) #beauty rest so we don't tire out the URL
    
print(months)
print(ios)
print(android)


# In[136]:


#Use subplots to plot both curves in the same figure
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.tools as tls
get_ipython().magic('matplotlib inline')
import datetime
import numpy as np
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


# fig, ax1 = plt.subplots(sharey=True)
fig, ax1 = plt.subplots()

#Set tick labels and rotate by 45 degrees for readability
years = mdates.YearLocator()   # every year
month = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y') 

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(yearsFmt)
ax1.xaxis.set_minor_locator(month)
ax1.yaxis.set_major_locator(ticker.LinearLocator())
fig.autofmt_xdate()


# ax1.plot(months, ios, 'r-', months, android, 'b-')

#Create legend
line_up, = plt.plot(months, ios, label='iOS')
line_down, = plt.plot(months, android, label='Android')
plt.legend([line_up, line_down], ['iOS', 'Android'])

#Label Axes
plt.ylabel('Market Share')
plt.xlabel('Year')

#Show plot
plt.show()

