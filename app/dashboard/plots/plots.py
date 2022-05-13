import sqlite3
from datetime import datetime
from monthly_spent_details import MonthlySpentDetails
from earnings_and_savings import EarningsAndSavings

class Plots:
    '''
    This class provides all the plot values for dashboard page.
    '''

    def __init__(self, db_path):
        '''
        Constructor method for Plots class.

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

    def get_monthly_spent_details(self):
        '''
        Driver method for MonthlySpentDetails class. 
        The output will contain :
            1. monthly spent details plot values
            2. current month amount spend
            3. current month total amount spend transactions count
            4. current month expenditure percentage (compared with previous month expenditure)

        :return: return all the outputs of 'MonthlySpentDetails' class
        :rtype: tuple
        '''

        try:
            monthly_spent_details = MonthlySpentDetails(self.__db_path)
        except Exception as e:
            print(e)
        else:
            day_values = monthly_spent_details.get_plot_values()
            month_money = monthly_spent_details.current_month_amount_spend()
            transaction_count = monthly_spent_details.current_month_transactions_count()
            expenditure = monthly_spent_details.current_month_expenditure_percentage()
        
        return day_values, month_money, transaction_count, expenditure

    def get_earnings_and_savings_report_values(self):
        '''
        Driver method for EarningsAndSavings class. 
        The output will contain :
            1. earnings and savings bar plot values
            2. current month savings value
            3. current month earnings percentage (compared with previous month percentage)
            4. current month savings percentage (compared with previous month percentage)

        :return: return outputs of 'EarningsAndSavings' class.
        :rtype: tuple
        '''

        try:
            earnings_and_savings = EarningsAndSavings(self.__db_path)
        except Exception as e:
            print(e)
        else:
            earnings_and_savings_values = earnings_and_savings.get_plot_values()
            current_month_savings = earnings_and_savings.current_month_savings()
            earnings_percentage = earnings_and_savings.current_month_earnings_percentage()
            savings_percentage = earnings_and_savings.current_month_savings_percentage()


        return earnings_and_savings_values, current_month_savings, earnings_percentage, savings_percentage

    def get_yearly_detail_report_values(self):
        '''
        This method return current year monthly amount spend values, monthly earnings values
        and monthly savings values to plot yearly detail report

        :return: return values required to plot yearly detail report
        :rtype: tuple
        '''

        cursor = self.__connection.cursor()
        previous_spend = self.__connection.cursor()
        year = datetime.today().year
        month = datetime.today().month
        monthly_amount_spends = []
        monthly_earnings = []
        monthly_savings = []

        # queries
        spend_query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month,CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        previous_spend_query = "select sum(m2.Amount) as Previous_Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month,CAST(substr(m1.'Date', 1, 4) as INT) as Year from previous_savings as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        earnings_query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Month in (?) and m2.Year in (?)"
        savings_query = "select Amount from savings where Month in (?) and Year in (?)"

        # retrieving month wise amount spend & previous savings spend
        for month in range(1, 13):
            # For Monthly spend
            try:
                cursor.execute(spend_query, (month, year))
                previous_spend.execute(previous_spend_query, (month, year))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                previous_saving_result = previous_spend.fetchone()

                # For Previous Savings Expenditure
                if previous_saving_result['Previous_Sum'] is None:
                    previous_savings_spend = 0
                else:
                    previous_savings_spend = int(previous_saving_result['Previous_Sum'])

                # For Monthly amount spend
                if result['Sum'] is None:
                    amount_spend = 0
                else:
                    amount_spend = int(result['Sum'])

                monthly_amount_spends.append(previous_savings_spend + amount_spend)

            # retrieving month wise earnings
            try:
                cursor.execute(earnings_query, (month, year))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Sum'] is None:
                    monthly_earning = 0
                else:
                    monthly_earning = int(result['Sum'])
                monthly_earnings.append(monthly_earning)
        
            # Retrieving month wise savings
            try:
                cursor.execute(savings_query, (month, year))
            except Exception as e:
                print(e)
            else:
                result = cursor.fetchone()
                if result['Amount'] is None:
                    monthly_saving = 0
                else:
                    monthly_saving = int(result['Amount'])

                monthly_savings.append(monthly_saving)

        return monthly_amount_spends, monthly_earnings, monthly_savings

if __name__ == "__main__":
    main_path = "/Users/srinivas/Desktop/M_Monitor/"
    file_name = "main_monitor.db"
    p = Plots(db_path=main_path+file_name)
    print(p.get_monthly_spent_details())
    print(p.get_earnings_and_savings_report_values())
    print(p.get_yearly_detail_report_values())