import sqlite3
from datetime import datetime

class EarningsAndSavings:
    '''
    This class represents Earnings and Savings Report present in dashboard Page
    '''

    def __init__(self, db_path):
        '''
        Constructor method for class EarningsAndSavings

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
        This method returns plot values of Earnings and Savings Report

        :return: return plot values of Earnings and Savings Report
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        # Current Year Monthly Earnings
        earnings_query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        earnings_values = []
        savings_values = []
        for i in range(1, 13):
            try:
                cursor.execute(earnings_query, (i, year))
            except Exception as e:
                print(e)
                break
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    earnings_values.append(0)
                else:
                    earnings_values.append(int(result['Sum']))

        # Current Year Monthly Amount Spend
        spend_query = "select Amount from savings where Month in (?) and Year in (?)"
        for i in range(1, 13):
            try:
                cursor.execute(spend_query, (i, year))
            except Exception as e:
                print(e)
                break
            else:
                result = cursor.fetchone()
                if result['Amount'] is None:
                    savings_values.append(0)
                else:
                    savings_values.append(int(result['Amount']))

        if len(earnings_values) != 12 or len(savings_values) != 12:
            pass
        else:
            earnings_and_savings = [['Month', 'Earnings', 'Savings']]
            if month in range(1, 6):
                for i in range(5):
                    earnings_and_savings.append([month_names[i], earnings_values[i], savings_values[i]])
            else:
                for i in range(month-5, month):
                    earnings_and_savings.append([month_names[i], earnings_values[i], savings_values[i]])
            return earnings_and_savings

    def current_month_savings(self):
        '''
        This method returns current month savings value

        :return: return current month savings value
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "select Amount from savings where Month in (?) and Year in (?)"
        try:
            cursor.execute(query, (month, year))
        except Exception as e:
            print(e)
        else:
            result = cursor.fetchone()
            if result['Amount'] is None:
                current_month_savings = 0
            else:
                current_month_savings = int(result['Amount'])
            return current_month_savings

    def current_month_earnings_percentage(self):
        '''
        This method returns current month earnings percentage value
        
        Positve percentage indicates the 'increase' in earnings compared to last month
        Negative percentage indicates the 'decrease' in earnings compared to last month

        :return: return current month earnings percentage value
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        earnings = []
        for i in range(month-1, month+1):
            try:
                cursor.execute(query, (i, year))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    earnings.append(0)
                else:
                    earnings.append(int(result['Sum']))

        if len(earnings) != 2:
            pass
        else:
            if earnings[0] == 0:
                earnings_percentage = 0
            else:
                earnings_percentage = int((earnings[1] - earnings[0]) / earnings[0] * 100)

            return earnings_percentage

    def current_month_savings_percentage(self):
        '''
        This method returns current month savings percentage values

        Positve percentage indicates the 'increase' in savings compared to last month
        Negative percentage indicates the 'decrease' in savings compared to last month

        :return: return current month savings percentage values
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "select Amount from savings where Month in (?) and Year in (?)"
        savings = []
        for i in range(month-1, month+1):
            try:
                cursor.execute(query, (i, year))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Amount'] is None:
                    savings.append(0)
                else:
                    savings.append(int(result['Amount']))

        if len(savings) != 2:
            pass
        else:
            if savings[0] == 0:
                savings_percentage = 0
            else:
                savings_percentage = int((savings[1] - savings[0]) / savings[0] * 100)

            return savings_percentage

if __name__ == "__main__":
    main_path = "/Users/srinivas/Desktop/M_Monitor/"
    file_name = "main_monitor.db"
    e = EarningsAndSavings(db_path=main_path+file_name)
    print(e.get_plot_values())
    print(e.current_month_savings())
    print(e.current_month_earnings_percentage())
    print(e.current_month_savings_percentage())
    # help(e)