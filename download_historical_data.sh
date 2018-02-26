#!/bin/bash

# Test
python getYahooFinanceData.py -c 1 -f stock_db/test.txt -d ./stock_db/test

# Questrade portfolio
python getYahooFinanceData.py -f stock_db/qt.txt -d ./stock_db/qt

# Dow Jones
python getYahooFinanceData.py -f stock_db/dj.txt -d ./stock_db/dj

# TSX
python getYahooFinanceData.py -f stock_db/tsx.txt -d ./stock_db/tsx

# SP-500
python getYahooFinanceData.py -f stock_db/sp500.txt -d ./stock_db/sp500
