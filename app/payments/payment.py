import sqlite3
from datetime import datetime
# from Payments.four_blocks.four_blocks import FourBlocks
from app.payments.four_blocks import FourBlocks

class Payment:
    '''
    This class represents payments page functions
    '''
    def __init__(self, db_path):
        '''
        Constructor Method For Class Payment

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

    def get_four_blocks(self):
        '''
        This method is the driver method for FourBlocks class
        This method returns current month payment mode wise amount spend like
        monthly_cash_spend, monthly_debit_spend etc.

        :return: returns current month payment mode wise amount spend
        :rtype: tuple
        '''
        try:
            four_blocks = FourBlocks(db_path=self.__db_path)
        except Exception as e:
            print("Function: get_four_blocks, Error: {e}")
            exit()
        else:
            month_cash_spend = four_blocks.monthly_cash_payments()
            month_debit_spend = four_blocks.monthly_debit_payments()
            month_credit_spend = four_blocks.monthly_credit_payments()
            month_upi_spend = four_blocks.monthly_upi_payments()

            return month_cash_spend, month_credit_spend, month_debit_spend, month_upi_spend

    def plot_amount_spent_payment_types(self):
        '''
        This method returns percentage values of payment mode wise amount spend like
        percentage values of monthly_cash_spend, monthly_debit_spend etc.

        :return: returns percentage values of payment mode wise amount spend
        :rtype: list
        '''
        cursor = self.__connection.cursor()
        month = datetime.today().month
        query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Payment_Mode in (?)"
        try:
            cursor.execute(query, (month, 'Phonpe UPI'))
        except sqlite3.Error as e:
            print(f"Function: plot_amount_spent_payment_types, Error: {e}")
        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                month_ppay_spend = 0
            else:
                month_ppay_spend = int(result['Sum'])
            
            try:
                month_cash_spend, month_credit_spend, month_debit_spend, month_upi_spend = self.get_four_blocks()
            except Exception as e:
                print(f"Function: plot_amount_spent_payment_types, Error: {e}")
                exit()
            else:
                month_gpay_spend = month_upi_spend - month_ppay_spend
                sum = month_cash_spend + month_credit_spend + month_debit_spend + month_upi_spend
                value = [month_cash_spend, month_credit_spend, month_debit_spend, month_ppay_spend, month_gpay_spend]
                if sum == 0:
                    percents = []
                else:
                    percents = [int(i/sum * 100) for i in value]

            return percents



# if __name__ == "__main__":
#     payment = Payment(db_path='main_monitor.db')
#     print(payment.get_four_blocks())
#     print(payment.plot_amount_spent_payment_types())
#     print(payment.db_path)
#     print(payment.connection)