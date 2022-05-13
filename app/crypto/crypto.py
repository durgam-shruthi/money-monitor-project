import sqlite3
from datetime import datetime
from app.crypto.four_blocks import FourBlocks

class Crypto:
    '''
    This class represents all the crypto page functions
    '''

    def __init__(self, db_path):
        '''
        Constructor Method For Class Crypto

        :param db_path: Input SQLite Database Path
        :type db_path: str
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
        :type new_db_path: str
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

    def get_four_blocks(self):
        '''
        This method is the driver method for FourBlocks class andreturns current month crypto 
        earnings information 

        This method calculates:
        
        1. today_crypto_earn
        2. month_crypto_count
        3. month_crypto_earn
        4. year_crypto_earn

        :return: returns current month crypto earnings information
        :rtype: tuple
        '''

        try:
            four_blocks = FourBlocks(db_path=self.__db_path)
        except Exception as e:
            print("Function: get_four_blocks, Error: {e}")
            exit()
        else:
            today_crypto_earn = four_blocks.current_day_earnings()
            month_crypto_count = four_blocks.current_month_transaction_count()
            month_crypto_earn = four_blocks.current_month_earnings()
            year_crypto_earn = four_blocks.current_year_earnings()

            return today_crypto_earn, month_crypto_count, month_crypto_earn, year_crypto_earn

    def plot_current_month_crypto_earnings(self):
        '''
        This method return current month daily 'crypto earnings' values to plot line chart

        :return: return current month daily crypto earnings values
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        day = datetime.today().day
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in (?)"
        daily_earned = []
        for i in range(1, day+1):
            try:
                cursor.execute(query, (month, i, 'Crypto Earning'))
            except sqlite3.Error as e:
                print(e)
                break
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    daily_earned.append(0)
                else:
                    daily_earned.append(result['Sum'])

        if len(daily_earned) != day:
            pass
        else:
            return daily_earned


    def get_latest_ten_earnings(self):
        '''
        This method returns latest ten crypto earning values

        :return: returns latest ten crypto earnings
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        query = "SELECT * FROM Earnings as a WHERE a.'S No'  > 0 and a.'Category' in ('Crypto Earning') ORDER BY a.'S No' DESC  LIMIT 10;"
        try:
            cursor.execute(query)
        except sqlite3.Error as e:
            print(e)
        else:
            output_rows = cursor.fetchall()
            return output_rows


if __name__ == "__main__":
    crypto = Crypto(db_path="/Users/srinivas/Desktop/M_Monitor/main_monitor.db")
    print(crypto.get_four_blocks())
    print(crypto.plot_current_month_crypto_earnings())
    print(crypto.get_latest_ten_earnings())