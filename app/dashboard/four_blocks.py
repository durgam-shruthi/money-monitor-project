import sqlite3
from datetime import datetime

class FourBlocks:
    '''
    This class represents the internal logic of fourblocks in dashboard page
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

    # add getters and setters for both attributes
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

    def current_day_amount_spent(self):
        '''
        This method return current day amount spent by the users

        :return: returns current day amount spent
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        day = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day,CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.day in (?) and m2.Month in (?) and m2.Year in (?) "
        try:
            cursor.execute(query, (day, month, year))
        except Exception as e:
            print(f"Class: app/dashboard/four_blocks.py, function: current_day_amount_spent, Error:{e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                today_amount = 0
            else:
                today_amount = int(result['Sum'])

            return today_amount

    def current_year_previous_savings(self):
        '''
        This method return current year total savings excluding current month savings.

        :return: return previous savings of current year (excluding current month)
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        # Calculate current year total savings and remove current month savings
        month = datetime.today().month
        year = datetime.today().year
        # Initially Assigning Values To None
        current_year_savings = None
        current_month_savings = None
        year_query = "select sum(Amount) as Sum from savings where Year in (?)"
        month_query = "select sum(Amount) as Sum from savings where Month in (?) and Year in (?)"
        try:
            cursor.execute(year_query, (year,))
        except Exception as e:
            print(f"Class: app/dashboard/four_blocks.py, function: current_year_previous_savings, Error:{e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                current_year_savings = 0
            else:
                current_year_savings = int(result['Sum'])

        try:
            cursor.execute(month_query, (month, year))
        except Exception as e:
            print(f"Class: app/dashboard/four_blocks.py, function: current_year_previous_savings, Error:{e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                current_month_savings = 0
            else:
                current_month_savings = int(result['Sum'])
        if current_year_savings is not None and current_month_savings is not None:
            previous_savings = current_year_savings - current_month_savings
            return previous_savings

    def current_day_earnings(self):
        '''
        This method return current day earning values

        :return: return current day earnings
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        day = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day,CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.day in (?) and m2.Month in (?) and m2.Year in (?)"
        try:
            cursor.execute(query, (day, month, year))
        except Exception as e:
            print(f"Class: app/dashboard/four_blocks.py, function: current_day_earnings, Error:{e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                current_day_earnings = 0
            else:
                current_day_earnings = int(result['Sum'])
        
            return current_day_earnings
        
    def current_month_earnings(self):
        '''
        This method return current month total earnings value.

        :return: return current month total earnings
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        try:
            cursor.execute(query, (month, year))
        except Exception as e:
            print(f"Class: app/dashboard/four_blocks.py, function: current_month_earnings, Error:{e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                month_earnings = 0
            else:
                month_earnings = int(result['Sum'])
        
            return month_earnings

# if __name__ == "__main__":
#     main_path = "/Users/srinivas/Desktop/M_Monitor/"
#     file_name = "main_monitor.db"
#     fblocks = FourBlocks(db_path=main_path+file_name)
#     print(fblocks.current_day_amount_spent())
#     print(fblocks.current_year_previous_savings())
#     print(fblocks.current_day_earnings())
#     print(fblocks.current_month_earnings())