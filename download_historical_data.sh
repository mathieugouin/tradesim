#!/bin/bash

# Test
echo Test
python getYahooFinanceData.py -c 1 -f stock_db/test.txt -d ./stock_db/test

# Indices
python getYahooFinanceData.py -c 1 -f stock_db/indices.txt -d ./stock_db/indices

# Questrade portfolio
echo Questrade
python getYahooFinanceData.py -f stock_db/qt.txt -d ./stock_db/qt

# Dow Jones
echo Dow Jones
python getYahooFinanceData.py -f stock_db/dj.txt -d ./stock_db/dj

# TSX
echo TSX
python getYahooFinanceData.py -f stock_db/tsx.txt -d ./stock_db/tsx

# SP-500
echo SP-500
python getYahooFinanceData.py -f stock_db/sp500.txt -d ./stock_db/sp500
