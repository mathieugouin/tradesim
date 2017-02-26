#!/usr/bin/env python

# TBD not completed....

import urllib
import xml.etree.ElementTree as ET

"""
This module provides a Python API for retrieving stock data from TMX
"""

# Using YQL:
#
# Stock Name:
# select * from html where url='http://mobile.tmxmoney.com/quote/?symbol=XBB' and xpath='/html/body/div[@id="qm-w"]/div[@class="mobi-wrapper"]/div[@id="qm-b"]/div[@class="qm-bw"]/div[@id="q-t"]/div/h3'
#
# Stock Data:
# select * from html where url='http://mobile.tmxmoney.com/quote/?symbol=NA' and xpath='/html/body/div[@id="qm-w"]/div[@class="mobi-wrapper"]/div[@id="qm-b"]/div[@class="qm-bw"]/div[@id="q-b"]/table[@id="detailedquote"]/tbody/tr/td/span[@class="l"]'


def yahoo_to_tmx_stock_name(symbol):
    # need to convert from
    # CP.TO to TSE:CP
    # PG to US:PG
    return symbol

def _get_url(url):
    tryAgain = True
    count = 0
    s = ""
    while tryAgain and count < 10:
        try:
            s = urllib.urlopen(url).read().strip()
            tryAgain = False
        except:
            print "Error, will try again"
            count += 1
    return s


def _get_xml(symbol):
    url = r'http://query.yahooapis.com/v1/public/yql?q=select * from google.igoogle.stock where stock="%s";&env=store://datatables.org/alltableswithkeys' % symbol.upper()
    xml = _get_url(url)
    return ET.fromstring(xml)


def _get_data(symbol, data):
    root = _get_xml(symbol)
    return root.findall('./results/xml_api_reply/finance/%s' % data)[0].attrib['data']


def get_all(symbol):
    root = _get_xml(symbol)
    data = {}
    for e in root.findall('./results/xml_api_reply/finance/*'):
        data[e.tag] = e.attrib['data']
    return data


def get_company_name(symbol):
    return _get_data(symbol, 'company')


def get_currency(symbol):
    return _get_data(symbol, 'currency')


def _main():
    print get_company_name("CP.TO")
    print get_currency("CP.TO")
    d = get_all("CP.TO")
    print d


if __name__ == '__main__':
    _main()
