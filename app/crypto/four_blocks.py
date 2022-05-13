import sqlite3
from datetime import datetime

class FourBlocks:
    '''
    This class returns values of four blocks for crypto page 
    '''

    def __init__(self, db_path):
        '''
        Constructor method for FourBlocks class 

        :param db_path: Input database path
        :type db_path: str
        :raises TypeError: Database path must be string
        :raises Exception: Enter valid database file path
        '''
        
        if type(db_path) != str:
            raise TypeError(f"Database Path Must Be String. Entered Wrong Input Type: {type(db_path)}")
        elif '.db' not in db_path.split('/')[-1]:
            raise Exception(f"Please Enter Database File Path. Entered File Path For: {db_path.split('/')[-1]}")
        else:
            self.__db_path = db_path
            self.__connection = sqlite3.connect(self.__db_path)
            self.__connection.row_factory = sqlite3.Row
  
    
    @property
    def db_path(self):
        '''
        Getter Method For db_path Attribute

        :return: Database path
        :rtype: str
        '''
        return self.__db_path


    @property
    def connection(self):
        '''
        Getter Method For Connection Attribute

        :return: Connection Object of SQLite3 Database
        :rtype: sqlite3.Connection object
        '''
        return self.__connection


    @db_path.setter
    def db_path(self, new_db_path):
        '''
        Setter Method For db_path Attribute

        :param new_db_path: Input SQLite Database Path
        :type new_db_path: String
        :raises TypeError: Database Path Must Be String
        :raises Exception: Entered File Path Should be For Database
        '''
        if type(new_db_path) != str:
            raise TypeError(f"New Input Must Be String. Entered Wrong Input Type: {type(new_db_path)}")
        elif '.db' not in new_db_path.split('/')[-1]:
            raise Exception(f"Please Enter Database File Path. Entered File Path For: {new_db_path.split('/')[-1]}")
        else:
            self.__db_path = new_db_path
            self.__connection = sqlite3.connect(self.__db_path)
            self.__connection.row_factory = sqlite3.Row


    def current_day_earnings(self):
        '''
        This method calculates current day crypto earnings

        :return: returns current day crypto earnings
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        day = datetime.today().day
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in (?)"
        try:
            cursor.execute(query, (month, day, 'Crypto Earning'))
        except sqlite3.Error as e:
            print(f"Function: current_day_earnings, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                today_crypto_earn = 0
            else:
                today_crypto_earn = int(result['Sum'])

        return today_crypto_earn


    def current_month_transaction_count(self):
        '''
        This method calculates current month total crypto earning transaction counts

        :return: returns current month total crypto earnings transaction counts
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select count(m2.Amount) as Count from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Category in (?) and m2.Month in (?)"
        try:
            cursor.execute(query, ('Crypto Earning', month))
        except sqlite3.Error as e:
            print(f"Function: current_month_transaction_count, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Count'] is None:
                month_crypto_count = 0
            else:
                month_crypto_count = int(result['Count'])

        return month_crypto_count


    def current_month_earnings(self):
        '''
        This method calculates current month total crypto earnings

        :return: returns current month total crypto earnings
        :rtype: int
        '''
        
        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select SUM(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Category in (?) and m2.Month in (?)"
        try:
            cursor.execute(query, ('Crypto Earning', month))
        except sqlite3.Error as e:
            print(f"Function: current_month_earnings, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                month_crypto_earn = 0
            else:
                month_crypto_earn = int(result['Sum'])

        return month_crypto_earn


    def current_year_earnings(self):
        '''
        This method calculates current year total crypto earnings

        :return: returns current year total crypto earnings
        :rtype: int
        '''
        
        cursor = self.__connection.cursor()
        year = datetime.today().year
        query = "select SUM(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Category in (?) and m2.Year in (?)"
        try:
            cursor.execute(query, ('Crypto Earning', year))
        except sqlite3.Error as e:
            print(f"Function: current_year_earnings, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                year_crypto_earn = 0
            else:
                year_crypto_earn = int(result['Sum'])

        return year_crypto_earn


if __name__ == "__main__":
    fblocks = FourBlocks(db_path="/Users/srinivas/Desktop/M_Monitor/main_monitor.db")
    print(fblocks.current_day_earnings())
    print(fblocks.current_month_earnings())
    print(fblocks.current_month_transaction_count())
    print(fblocks.current_year_earnings())
