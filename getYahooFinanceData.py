#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Reference:
# http://code.google.com/p/yahoo-finance-managed/wiki/csvHistQuotesDownload

__author__ = 'gian paolo ciceri <gp.ciceri@gmail.com>'
__version__ = '0.1'
__date__ = '20070401'
__credits__ = "queue and MT code was shamelessly stolen from pycurl example retriever-multi.py"

#
# Usage: python getYahooFinanceData.py -h
#
#
# for selecting tickers and starting date it uses an input file of this format
# <ticker> <fromdate as YYYYMMDD>
# like
# ^GSPC 19500103 # S&P 500
# ^N225 19840104 # Nikkei 225

# System
import sys
import threading
import Queue
import datetime
import traceback
import urllib
from optparse import OptionParser
import os

# User
import yqd

# this thread ask the queue for job and does it!
class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            try:
                # fetch a job from the queue
                ticker, fromdate, todate = self.queue.get_nowait()
            except Queue.Empty:
                raise SystemExit
            if ticker[0] == "^": # make sure filename compatible
                filenameTicker = ticker[1:]
            else:
                filenameTicker = ticker

            if options.verbose:
                print "ticker:", ticker
                print "last date asked:", todate, todate[0:4], todate[4:6], todate[6:8]
                print "first date asked:", fromdate, fromdate[0:4], fromdate[4:6], fromdate[6:8]

            if not options.offline:
                # download ticker data using yqd
                alllines = yqd.load_yahoo_quote(ticker, fromdate, todate)

                if len(alllines) > 5: # safety check
                    filename = os.path.join(options.downloadTo, filenameTicker + '.csv')
                    fp = open(filename, "wb")
                    fp.write(alllines)
                    fp.close()

            if options.verbose:
                print "fetched: ", ticker
            else:
                sys.stdout.write(".")
                sys.stdout.flush()

if __name__ == '__main__':
    # today is
    today = datetime.datetime.now().strftime("%Y%m%d")
    # default start date (very early to get all possible data)
    startdate = datetime.date(1900, 1, 1).strftime("%Y%m%d")

    # parse arguments
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="tickerfile", action="store", default = "./tickers.txt",
                      help="read ticker list from file, it uses ./tickers.txt as default")
    parser.add_option("-c", "--concurrent", type="int", dest="connections", default = 10, action="store",
                      help="# of concurrent connections")
    parser.add_option("-d", "--dir", dest="downloadTo", action="store", default = "./rawdata/",
                      help="save data to this directory, it uses ./rawdata/ as default")

    parser.add_option("-s", "--startdate", dest="startdate", default = startdate, action="store",
                      help="start date, format is YYYYMMDD, ex: 19991231")
    parser.add_option("-t", "--todate", dest="todate", default = today, action="store",
                      help="most recent date needed, format is YYYYMMDD, ex: 20121231")
    parser.add_option("-v", "--verbose", default = False,
                          action="store_true", dest="verbose")
    parser.add_option("-o", "--offline", default = False,
                          action="store_true", dest="offline")

    (options, args) = parser.parse_args()

    # get input list
    try:
        f = open(options.tickerfile, 'r')
        tickers = f.readlines()
        f.close()
    except:
        parser.error("ticker file %s not found" % (options.tickerfile))
        raise SystemExit

    # build a queue with (ticker, fromdate, todate) tuples
    queue = Queue.Queue()
    for tickerRow in tickers:
        #print tickerRow
        tickerRow = tickerRow.strip() # remove leading and trailing whitespace
        if not tickerRow or tickerRow[0] == "#":  # skip comment line starting with #
            continue
        tickerSplit = tickerRow.split() # split on whitespace to ignore optional description after the ticker

        if options.verbose:
            print "Adding (ticker, startdate, todate):",\
                tickerSplit[0], options.startdate, options.todate

        # ticker, fromdate, todate
        queue.put((tickerSplit[0], options.startdate, options.todate))

    # Check args
    assert queue.queue, "no Tickers given"
    numTickers = len(queue.queue)
    connections = min(options.connections, numTickers)
    assert 1 <= connections <= 255, "too much concurrent connections asked"

    if options.verbose:
        print "----- Getting", numTickers, "Tickers using", connections, "simultaneous connections -----"

    # At this point, get a dummy small quote from Y! to get the crumb & cookie before the threads start
    assert len(yqd.load_yahoo_quote('^GSPC', '20180212', '20180212')) > 5, "Error: initial download did not work"

    # start a bunch of threads, passing them the queue of jobs to do
    threads = []
    for dummy in range(connections):
        t = WorkerThread(queue)
        t.start()
        threads.append(t)

    # wait for all threads to finish
    for thread in threads:
        thread.join()
    sys.stdout.write("\n")
    sys.stdout.flush()

    # tell something to the user before exiting
    if options.verbose:
        print "all threads are finished - goodbye."
