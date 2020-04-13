#! /usr/bin/env python

"""Yahoo historical quotes downloader.

Reference:
http://code.google.com/p/yahoo-finance-managed/wiki/csvHistQuotesDownload

Usage: python get_yahoo_finance_data.py -h

For selecting tickers and starting date it uses an input file of this format
<ticker> <fromdate as YYYYMMDD>
like
^GSPC 19500103 # S&P 500
^N225 19840104 # Nikkei 225
"""

# To make print working for Python2/3
from __future__ import print_function

# System
import sys
import threading
import Queue
import datetime
import argparse
import os

# User
import yqd


def _my_assert(expression, msg='No message provided'):
    if not expression:
        raise AssertionError(msg)


class WorkerThread(threading.Thread):
    """Thread class to ask the queue for job and does it."""

    def __init__(self, queue):
        """Creates a new thread."""
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
                filename_ticker = ticker[1:]
            else:
                filename_ticker = ticker

            if options.verbose:
                print("ticker:", ticker)
                print("last date asked:", todate, todate[0:4], todate[4:6], todate[6:8])
                print("first date asked:", fromdate, fromdate[0:4], fromdate[4:6], fromdate[6:8])

            if not options.offline:
                # download ticker data using yqd
                all_lines = yqd.load_yahoo_quote(ticker, fromdate, todate)

                if len(all_lines) > 5: # safety check
                    filename = os.path.join(options.dir, filename_ticker + '.csv')
                    fp = open(filename, "wb")
                    fp.write(all_lines)
                    fp.close()

            if options.verbose:
                print("fetched: ", ticker)
            else:
                sys.stdout.write(".")
                sys.stdout.flush()


if __name__ == '__main__':
    # today is
    today = datetime.datetime.now().strftime("%Y%m%d")
    # default start date (very early to get all possible data)
    start_date = datetime.date(1900, 1, 1).strftime("%Y%m%d")

    # parse arguments
    parser = argparse.ArgumentParser(description='Yahoo historical quotes downloader')
    parser.add_argument('-f', '--file', action='store', default='./tickers.txt',
                        help='read ticker list from file, it uses ./tickers.txt as default')
    parser.add_argument('-c', '--concurrent', type=int, default=10,
                        action='store', help='# of concurrent connections used for the download')
    parser.add_argument('-d', '--dir', action='store', default='./rawdata',
                        help='save data to this directory, it uses ./rawdata/ as default')
    parser.add_argument('-s', '--startdate', default=start_date, action='store',
                        help='start date, format is YYYYMMDD, default is ' + start_date)
    parser.add_argument('-t', '--todate', default=today, action='store',
                        help='most recent date, format is YYYYMMDD, default is ' + today)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='explain what is being done')
    parser.add_argument('-o', '--offline', action='store_true',
                        help='used for testing, skip the actual downloading')

    options = parser.parse_args()

    if options.verbose:
        print('Command line options parsed successfully.')

    # get input list
    with open(options.file, 'r') as f:
        ticker_lines = f.readlines()

    # build a queue with (ticker, fromdate, todate) tuples
    queue = Queue.Queue()
    for line in ticker_lines:
        line = line.strip() # remove leading and trailing whitespace
        # skip empty lines or line starting with # (comment)
        if not line or line[0] == "#":
            if options.verbose:
                print('Skipping ticker file line: ' + line)
            continue
        # split on whitespace to ignore optional description after the ticker
        ticker = line.split()[0]

        if options.verbose:
            print("Adding {} from {} to {}".format(ticker, options.startdate, options.todate))

        queue.put((ticker, options.startdate, options.todate))

    # Check args
    _my_assert(queue.queue, "no Tickers given")
    nb_tickers = len(queue.queue)
    connections = min(options.concurrent, nb_tickers)
    _my_assert(1 <= connections <= 255, "too much concurrent connections asked")

    if options.verbose:
        print("----- Getting {} tickers using {} simultaneous connections -----".format(
            nb_tickers, connections))

    # Get a dummy small quote from Y! to get the crumb & cookie before the threads start.
    _my_assert(len(yqd.load_yahoo_quote('^GSPC', '20180212', '20180212')) > 5,
               "Error: initial download did not work")

    # start a bunch of threads, passing them the queue of jobs to do
    threads = []
    for _dummy in range(connections):
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
        print("all threads are finished - goodbye.")
