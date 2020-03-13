#!/bin/bash

echo Test
python getYahooFinanceData.py -c 1 -f stock_db/test.txt -d ./stock_db/test

echo Indices
python getYahooFinanceData.py -c 1 -f stock_db/indices.txt -d ./stock_db/indices

echo Questrade
python getYahooFinanceData.py -f stock_db/qt.txt -d ./stock_db/qt

echo Dow Jones
python getYahooFinanceData.py -f stock_db/dj.txt -d ./stock_db/dj

echo TSX
python getYahooFinanceData.py -f stock_db/tsx.txt -d ./stock_db/tsx

echo SP-500
python getYahooFinanceData.py -f stock_db/sp500.txt -d ./stock_db/sp500
