#!/usr/bin/env python
"""Date plots demo in matplotlib using date tick locators and formatters.

See major_minor_demo1.py for more information on controlling major and minor ticks.

All matplotlib date plotting is done by converting date instances into
days since the 0001-01-01 UTC.  The conversion, tick locating and
formatting is done behind the scenes so this is most transparent to
you.  The dates module provides several converter functions date2num
and num2date

This example requires an active internet connection since it uses
yahoo finance to get the data for plotting
"""

import datetime
from pylab import figure, show
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter

import parent_import
import stock_db_mgr as sdm


# format the coords message box
def price(x):
    return '$%1.2f' % x


date1 = datetime.date(1995, 1, 1)
date2 = datetime.date(2004, 4, 12)

db = sdm.StockDBMgr('stock_db/test', date1, date2)

years = YearLocator()   # every year
months = MonthLocator()  # every month
yearsFmt = DateFormatter('%Y')

df = db.get_symbol_data('SPY')

dates = [d for d in df.index]
opens = [o for o in df.loc[:, 'Open'].values]

fig = figure()
ax = fig.add_subplot(111)
ax.plot_date(dates, opens, '-')

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

ax.fmt_xdata = DateFormatter('%Y-%m-%d')
ax.fmt_ydata = price
ax.grid(True)

fig.autofmt_xdate()
show()
