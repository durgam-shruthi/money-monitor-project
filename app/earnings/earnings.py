import sqlite3
from datetime import datetime

class Earnings:
    '''
    This Class represents the Earnings Page Functions
    '''

    def __init__(self, db_path):
        '''
        Constructor Method For Class Earnings

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


    def individual_earnings_info(self):
        '''
        Returns Current Month Individual User Earnings Values To Display in First Row Cards

        This function will first retrieve user names from the Earnings table in database. 
        Then calculates the Individual User Earnings. 
        This values will be displayed in the first row cards of Earnings page.


        :raises Exception: Users Not Found In Table Earnings.
        :return: Individual User Earnings values in the form of dict.
        :rtype: dict
        '''

        cursor = self.__connection.cursor()
        Month = datetime.today().month
        # Fetching User Names From Database
        Query_For_Retrieval = "SELECT DISTINCT(a.User) as Name FROM Earnings as a"
        try:
            cursor.execute(Query_For_Retrieval)

        except sqlite3.Error as e:
            print(f"Function: person_wise_earnings, Error: {e}")

        else:
            result = cursor.fetchall()
            People_Names = [i['Name'] for i in result]
            if People_Names == []:
                raise Exception("Function: individual_earnings_info, Error: No Users in Database. Please Check Your Database")
            else:
                values = {}
                Query = '''select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month 
                from Earnings as m1) as m2 Where m2.Month in (?) and m2.User in (?)'''

                for name in People_Names:
                    try:
                        cursor.execute(Query, (Month, name))
                    except sqlite3.Error as e:
                        print(f"Function: individual_earnings_info, Error: {e}")
                        break
                    else:
                        result = cursor.fetchone()
                        if result['Sum'] is None:
                            values[name] = 0
                        else:
                            values[name] = int(result['Sum'])
                
                if len(values) != len(People_Names):
                    print("Please Resolve The Above Error!!. This Function Doesn't Returned Any Output")
                else:
                    return values


    def plot_person_wise_earnings(self):
        '''
        Returns Current Month Individual User Earnings Percentage Values To Plot 
        Individual User Earnings Donut Chart

        This function will first retrieve user names from the Earnings table in database. 
        Then calculates the Individual User Earnings Percentages. 
        This values will be used to plot Donut Chart


        :raises Exception: Users Not Found In Table Earnings
        :return: Individual User Earnings Percentages, User Names (percents, user_names)
        :rtype: list, list
        '''
        
        cursor = self.__connection.cursor()
        Month = datetime.today().month
        # Fetching User Names From Database
        Query_For_Retrieval = "SELECT DISTINCT(a.User) as Name FROM Earnings as a"

        try:
            cursor.execute(Query_For_Retrieval)

        except sqlite3.Error as e:
            print(f"Function: plot_person_wise_earnings, Error: {e}")

        else:
            result = cursor.fetchall()
            People_Names = [i['Name'] for i in result]

            if People_Names == []:
                raise Exception("Function: plot_person_wise_earnings, Error: No Users in Database to Calculate Individual User Earnings Percentage")
                
            # Calculating Percentages of User
            else:
                values = []
                Query = '''select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month 
                from Earnings as m1) as m2 Where m2.Month in (?) and m2.User in (?)'''

                for name in People_Names:
                    try:
                        cursor.execute(Query, (Month, name))
                    except sqlite3.Error as e:
                        print(f"Function: plot_person_wise_earnings, Error: {e}")
                        break
                    else:
                        result = cursor.fetchone()
                        if result['Sum'] is None:
                            values.append(0)
                        else:
                            values.append(result['Sum'])

                if len(values) != len(People_Names):
                    print("Please Resolve The Above Error!!. This Function Doesn't Returned Any Output")

                elif sum(values) == 0:
                    # Log That This months Earnings are empty
                    return values, People_Names

                else:
                    total_sum = sum(values)
                    percents = [int(i/total_sum * 100) for i in values]
                    return percents, People_Names


    def plot_category_wise_earnings(self):
        '''
        Returns Current Month Individual Category Earnings Percentage Values To Plot 
        Category Wise Earnings Donut Chart

        This function will first retrieve category names from the Earnings table in database. 
        Then calculates the Individual Category Earnings Percentages. 
        This values will be used to plot Donut Chart


        :raises Exception: Categories Not Found In Table Earnings
        :return: Individual Category Earnings Percentages, Category Names (percents, category_names)
        :rtype: list, list
        '''

        cursor = self.__connection.cursor()
        Month = datetime.today().month

        # Fetching Categories Names From Database
        Query_For_Retrieval = "SELECT DISTINCT(a.Category) as Category FROM Earnings as a"

        try:
            cursor.execute(Query_For_Retrieval)

        except sqlite3.Error as e:
            print(f"Function: plot_category_wise_earnings, Error: {e}")

        else:
            result = cursor.fetchall()
            Category_Names = [i['Category'] for i in result]

            if Category_Names == []:
                raise Exception("Function: plot_category_wise_earnings, Error: No Categories in Database to Calculate Categories Wise Earnings Percentage")
                
            # Calculating Percentages of User
            else:
                values = []
                Query = '''select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month 
                from Earnings as m1) as m2 Where m2.Month in (?) and m2.Category in (?)'''

                for category in Category_Names:
                    try:
                        cursor.execute(Query, (Month, category))
                    except sqlite3.Error as e:
                        print(f"Function: plot_category_wise_earnings, Error: {e}")
                        break
                    else:
                        result = cursor.fetchone()
                        if result['Sum'] is None:
                            values.append(0)
                        else:
                            values.append(result['Sum'])

                if len(values) != len(Category_Names):
                    print("Please Resolve The Above Error!!. This Function Doesn't Returned Any Output")

                elif sum(values) == 0:
                    # Log That This months Earnings are empty
                    return values, Category_Names

                else:
                    total_sum = sum(values)
                    percents = [int(i/total_sum * 100) for i in values]
                    return percents, Category_Names


    def plot_monthly_earnings(self):
        '''
        Returns Current Month's Day Wise Earning's Sum Upto Current Day. 
        This Values are used to Plot Monthly Earnings Plot.

        :return: Current Months Day Wise Earning's Sum Upto Today.
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        Month = datetime.today().month
        Day = datetime.today().day
        monthly_earnings = []
        Query = '''select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, 
        CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 
        Where m2.Month in (?) and m2.day in (?)'''

        for i in range(1, Day+1):
            try:
                cursor.execute(Query, (Month, i))
            except sqlite3.Error as e:
                print(e)
                break
            else:
                value = cursor.fetchall()
                if value[0]['Sum'] is None:
                    monthly_earnings.append(0)
                else:
                    monthly_earnings.append(value[0]['Sum'])

        if len(monthly_earnings) != Day:
            pass
        
        else:
            # print(monthly_earnings)
            return monthly_earnings


    def display_table(self):
        '''
        This function returns last 15 rows of Earnings table

        :return: Last 15 rows of Earnings Table
        :rtype: list
        '''

        cursor = self.__connection.cursor()
        try:
            Query = '''SELECT a.Date, a.User, a.Category, a.Amount, a.Amount_Form FROM Earnings as a 
            ORDER BY a.'S No' DESC  LIMIT 15;'''
            cursor.execute(Query)

        except sqlite3.Error as e:
            print(e)

        else:
            output_rows = cursor.fetchall()
            return output_rows



if __name__ == "__main__":
    e = Earnings("main_monitor.db")
    print(e.individual_earnings_info())
    print(e.plot_category_wise_earnings())
    # print(e.plot_person_wise_earnings())
    # print(e.display_table())
    # print(e.plot_monthly_earnings())

    ''' Next Steps
    1. Increase No Of Categories Of Earnings
    I Should Change the 3 Blocks Method. 
    
        1. I Should Add One More BLock Called Srinu Given Earnings.
        2. I Should Change Calculated Method for 3 Blocks. For Each Individual Person
        I should sum up Only Personal, Salary and Crypto Earnings. 

    2. Add Last Months Earnings Graph to Current Month Earnings Graph

    '''

    print(e.db_path)
    print(e.connection, type(e.connection))
