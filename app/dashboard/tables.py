import sqlite3
from datetime import datetime

class Tables:
    '''
    This class returns values of tables for dashboard page 
    '''

    def __init__(self, db_path):
        '''
        Constructor method for Table class

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

    def get_category_wise_expenditures(self):
        '''
        This method returns category wise expenditure rows
        Each row contains Category, Amount, Amount_Previous (Last Month), Expenditure Percentage 

        :return: category wise expenditure rows
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        month = datetime.today().month
        year = datetime.today().year
        query = "SELECT m1.Category, m1.Amount, m2.Amount as Amount_Previous, CAST(((m1.Amount - m2.Amount) / m2.Amount * 100) as INT) as Percentage FROM (SELECT Category, Amount  FROM monthly_data  WHERE Month = ? and Year = ? ) as m1 JOIN (SELECT Category , Amount FROM monthly_data  WHERE Month = ? and Year = ? ) as m2 ON (m1.Category = m2.Category);"
        if month == 1:
            try:
                cursor.execute(query, (month, year, 12, year-1))
            except Exception as e:
                print(e)
            else:
                categories = cursor.fetchall()
                return categories
        else:
            try:
                cursor.execute(query, (month, year, month-1, year))
            except Exception as e:
                print(e)
            else:
                categories = cursor.fetchall()
                return categories
  
    def get_latest_ten_amount_spends(self):
        '''
        This method returns latest ten amount spend rows

        :return: return latest ten amount spend rows
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        query = "SELECT * FROM amount_spend as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC  LIMIT 10 ;"
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
        else:
            rows = cursor.fetchall()
            return rows

if __name__ == "__main__":
    main_path = "/Users/srinivas/Desktop/M_Monitor/"
    file_name = "main_monitor.db"
    t = Tables(db_path=main_path+file_name)
    print(t.get_category_wise_expenditures())
    print(t.get_latest_ten_amount_spends())