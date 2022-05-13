import sqlite3
from datetime import datetime

class Recharge:
    '''
    This class represents all the other recharge page functions
    '''

    def __init__(self, db_path):
        '''
        Constructor Method For Class Recharge

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

    def plot_current_month_daily_spend(self):
        '''
        This method returns current month daily amount spend on 'Digital Recharge' category values 
        to plot line chart

        :return: returns current month daily amount spend on 'Digital Recharge' category values
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        day = datetime.today().day
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in (?)"
        daily_spend = []
        for i in range(1, day+1):
            try:
                cursor.execute(query, (month, i, 'Digital Recharge'))
            except sqlite3.Error as e:
                print(e)
                break
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    daily_spend.append(0)
                else:
                    daily_spend.append(result['Sum'])

        if len(daily_spend) != day:
            pass
        else:
            return daily_spend

    def get_latest_ten_spends(self):
        '''
        This method returns latest 10 amount spent transactions in 'Digital Recharge' category

        :return: returns latest 10 amount spent transactions in 'Digital Recharge' category
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        query = "SELECT * FROM amount_spend as a WHERE a.'S No' > 0 and a.'Category' in ('Digital Recharge') ORDER BY a.'S No' DESC  LIMIT 10;"
        try:
            cursor.execute(query)
        except sqlite3.Error as e:
            print(e)
        else:
            output_rows = cursor.fetchall()
            return output_rows

if __name__ == "__main__":
    recharge = Recharge(db_path="/Users/srinivas/Desktop/M_Monitor/main_monitor.db")
    print(recharge.plot_current_month_daily_spend())
    print(recharge.get_latest_ten_spends())
    print(recharge.db_path)
    print(recharge.connection)