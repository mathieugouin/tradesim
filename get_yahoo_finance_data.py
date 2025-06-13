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

# System
import sys
import threading
import datetime
import argparse
import os
import queue as queue_lib
# User
import yqd


# global options
options = None


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
            except queue_lib.Empty:
                raise SystemExit
            if ticker[0] == "^":  # make sure filename compatible
                filename_ticker = '_' + ticker[1:]
            else:
                filename_ticker = ticker

            if options.verbose:
                print("ticker:", ticker)
                print("last date asked: " + todate)
                print("first date asked: " + fromdate)

            if not options.offline:
                # download ticker data using yqd
                filename = os.path.join(options.dir, filename_ticker + '.csv')
                yqd.load_yahoo_quote(ticker, fromdate, todate, filename)

            if options.verbose:
                print("fetched: " + ticker)
            else:
                sys.stdout.write(".")
                sys.stdout.flush()


def _main():
    global options

    # today is
    today = datetime.datetime.now().strftime("%Y%m%d")
    # default start date (very early to get all possible data)
    start_date = datetime.date(1900, 1, 1).strftime("%Y%m%d")

    # parse arguments
    parser = argparse.ArgumentParser(description='Yahoo historical quotes downloader')
    parser.add_argument('-f', '--file', action='store', default='./tickers.txt',
                        help='read ticker list from file, it uses ./tickers.txt as default')
    parser.add_argument('-c', '--concurrent', type=int, default=1,
                        action='store', help='Number of concurrent connections used for the download. '
                        'This option is kept for backward compatibility.  Only 1 connection is used.')
    parser.add_argument('-d', '--dir', action='store', default='./rawdata',
                        help='save data to this directory, it uses ./rawdata/ as default')
    parser.add_argument('-s', '--startdate', default=start_date, action='store',
                        help='start date, format is YYYYMMDD, default is ' + start_date)
    parser.add_argument('-t', '--todate', default=today, action='store',
                        help='most recent date, format is YYYYMMDD, default is today: ' + today)
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
    queue = queue_lib.Queue()
    for line in ticker_lines:
        line = line.strip()  # remove leading and trailing whitespace
        # skip empty lines or line starting with  # (comment)
        if not line or line[0] == "#":
            if options.verbose:
                print('Skipping ticker file line: ' + line)
            continue
        # split on whitespace to ignore optional description after the ticker
        ticker = line.split()[0]

        if options.verbose:
            print(f"Adding {ticker} from {options.startdate} to {options.todate}")

        queue.put((ticker, options.startdate, options.todate))

    # Check args
    _my_assert(queue.queue, "no Tickers given")
    nb_tickers = len(queue.queue)
    # connections = min(options.concurrent, nb_tickers)
    # Force to 1 connections, yfinance does not seem to support multithreading
    connections = 1
    # _my_assert(1 <= connections <= 255, "too much concurrent connections asked")

    if options.verbose:
        print(f"----- Getting {nb_tickers} tickers using {connections} simultaneous connections -----")

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


if __name__ == '__main__':
    _main()
