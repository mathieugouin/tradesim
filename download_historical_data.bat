rem Questrade portfolio
python getYahooFinanceData.py -f stock_db/qt.txt -d ./stock_db/qt/

rem Dow Jones
python getYahooFinanceData.py -f stock_db/dj.txt -d ./stock_db/dj/

rem TSX
python getYahooFinanceData.py -f stock_db/tsx.txt -d ./stock_db/tsx/

rem SP-500
python getYahooFinanceData.py -f stock_db/sp500.txt -d ./stock_db/sp500/

pause

