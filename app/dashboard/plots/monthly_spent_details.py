import sqlite3
from datetime import datetime

class MonthlySpentDetails:
    '''
    This class represents the monthly spent details block in dashboard page
    '''
    
    def __init__(self, db_path):
        '''
        Constructor method for class MonthlySpentDetails

        :param db_path: Input SQLite Database Path
        :type db_path: String
        :raises TypeError: Database Path Must Be String
        :raises Exception: Entered File Path Should be For Database
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

    def get_plot_values(self):
        '''
        This method returns current month day wise amount spend values

        :return: return current month day wise amount spend values
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        day = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Year in (?)"
        day_values = []
        for i in range(1, day+1):

            try:
                cursor.execute(query, (month, i, year))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    day_values.append(0)
                else:
                    day_values.append(int(result['Sum']))

        if len(day_values) != day:
            pass
        else:
            return day_values

    def current_month_amount_spend(self):
        '''
        This method returns current month total amount spend

        :return: returns current month total amount spend
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        try:
            cursor.execute(query, (month, year))
        except Exception as e:
            print(e)
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                month_money = 0
            else:
                month_money = int(result['Sum'])

            return month_money

    def current_month_transactions_count(self):
        '''
        This method returns current month total transactions count

        :return: return current month transactions count
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "select count(m2.Amount) as Count from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        try:
            cursor.execute(query, (month, year))
        except Exception as e:
            print(e)
        else:
            result = cursor.fetchone()
            if result['Count'] is None:
                transaction_count = 0
            else:
                transaction_count = int(result['Count'])

            return transaction_count

    def current_month_expenditure_percentage(self):
        '''
        This method returns current month expenditure percentage

        Positve percentage indicates the 'increase' in expenditure compared to last month
        Negative percentage indicates the 'decrease' in expenditure compared to last month

        :return: returns current month expenditure percentage
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        last_month_money = None
        # Retrieving last Month Amount Spend
        last_month_query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        if month == 1:
            try:
                cursor.execute(last_month_query, (12, year-1))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    last_month_money = 0
                else:
                    last_month_money = int(result['Sum'])
        else:
            try:
               cursor.execute(last_month_query, (month-1, year)) 
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    last_month_money = 0
                else:
                    last_month_money = int(result['Sum'])

        # Retrieving Current Month Amount Spend
        try:
            month_money = self.current_month_amount_spend()
        except Exception as e:
            print(e)
            pass
        else:
            if last_month_money is None:
                pass
            elif last_month_money == 0:
                expenditure = 0
                return expenditure
            else:
                expenditure = int(((month_money - last_month_money) / last_month_money) * 100)
                return expenditure
            
if __name__ == "__main__":
    main_path = "/Users/srinivas/Desktop/M_Monitor/"
    file_name = "main_monitor.db"
    m = MonthlySpentDetails(db_path=main_path+file_name)
    print(m.get_plot_values())
    print(m.current_month_amount_spend())
    print(m.current_month_transactions_count())
    print(m.current_month_expenditure_percentage())