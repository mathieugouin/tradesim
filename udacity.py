# For online course: https://classroom.udacity.com/courses/ud501

import datetime
import stock_db_mgr as sdm


def test():
    pass


def _main():
    startdate = datetime.date(2004, 1, 1)
    enddate = datetime.date.today()

    # Create data base:
    db = sdm.CStockDBMgr('./stock_db/test', startdate, enddate)
    df = db.getSymbolData('SPY')
    print df.head()
    print df.describe()

    df = db.getAllSymbolDataSingleItem('Close')

    print df.head()
    print df.tail()

    pass


if __name__ == '__main__':
    _main()
