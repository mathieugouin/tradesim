#!/bin/bash

echo Test
python get_yahoo_finance_data.py --concurrent 1 --file stock_db/test.txt --dir ./stock_db/test

echo Indices
python get_yahoo_finance_data.py --concurrent 1 --file stock_db/indices.txt --dir ./stock_db/indices

echo Questrade
python get_yahoo_finance_data.py --concurrent 1 --file stock_db/qt.txt --dir ./stock_db/qt

echo Dow Jones
python get_yahoo_finance_data.py --concurrent 10 --file stock_db/dj.txt --dir ./stock_db/dj

echo TSX
python get_yahoo_finance_data.py --concurrent 10 --file stock_db/tsx.txt --dir ./stock_db/tsx

echo SP-500
python get_yahoo_finance_data.py --concurrent 30 --file stock_db/sp500.txt --dir ./stock_db/sp500
