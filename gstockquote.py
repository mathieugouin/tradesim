#!/usr/bin/env python
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib
import xml.etree.ElementTree as ET

"""
This is the "gstockquote" module.

This module provides a Python API for retrieving stock data from Google Finance.

sample usage:
>>> import gstockquote
>>> print gstockquote.get_price('GOOG')
529.46
"""


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
    #print get_company_name("CP.TO")
    #print get_currency('CP.TO')
    d = get_all("TSE:CP")
    print d


if __name__ == '__main__':
    _main()
