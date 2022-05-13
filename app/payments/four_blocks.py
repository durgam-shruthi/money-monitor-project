import sqlite3
from datetime import datetime

class FourBlocks:
    '''
    This class returns values of four blocks for payments page 
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


    def monthly_cash_payments(self):
        '''
        this method calculates current month payments made using cash

        :return: return current month amount spend using cash value
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Payment_Mode in (?)"
        try:
            cursor.execute(query, (month, 'Cash'))
        except sqlite3.Error as e:
            print(f"Function: monthly_cash_payments, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                monthly_cash = 0
            else:
                monthly_cash = int(result['Sum'])
            return monthly_cash


    def monthly_credit_payments(self):
        '''
        this method calculates current month payments made using credit card

        :return: return current month amount spend using credit card value
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Payment_Mode in (?)"
        try:
            cursor.execute(query, (month, 'Credit Card'))
        except sqlite3.Error as e:
            print(f"Function: monthly_credit_payments, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                monthly_credit= 0
            else:
                monthly_credit = int(result['Sum'])
            return monthly_credit


    def monthly_debit_payments(self):
        '''
        this method calculates current month payments made using debit card

        :return: return current month amount spend using debit card value
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Payment_Mode in (?)"
        try:
            cursor.execute(query, (month, 'Debit Card'))
        except sqlite3.Error as e:
            print(f"Function: monthly_debit_payments, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                monthly_debit= 0
            else:
                monthly_debit = int(result['Sum'])
            return monthly_debit


    def monthly_upi_payments(self):
        '''
        this method calculates current month payments made using UPI

        :return: return current month amount spend using UPI value
        :rtype: int
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Payment_Mode in (?, ?)"
        try:
            cursor.execute(query, (month, 'Phonpe UPI', 'Google Pay UPI'))
        except sqlite3.Error as e:
            print(f"Function: monthly_upi_payments, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                monthly_upi= 0
            else:
                monthly_upi = int(result['Sum'])
            return monthly_upi


if __name__ == "__main__":
    f = FourBlocks(db_path="main_monitor.db")
    # print(f.monthly_cash_payments())
    # print(f.monthly_credit_payments())
    # print(f.monthly_debit_payments())
    # print(f.monthly_upi_payments())
    # print(f.db_path)
    # print(f.connection)
