import sqlite3
from datetime import datetime
from app.earnings.earnings import Earnings

class Earnings_V2(Earnings):
    '''
    This class is the extension of Earnings Class

    :param Earnings: The Parent Class
    :type Earnings: Class Object
    '''

    def __init__(self, db_path):
        '''
        Constructor Method For CLass Earnings_V2

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
            Earnings.__init__(self, db_path)


    def individual_earnings_info(self, ignore_category="Srinu Given"):
        '''
        This is Modified Method in Parent Class: Earnings

        Returns current month individual user values to display in first three cards.
        This function calculates only individual earnings like (Personal, Salary, Crypto etc.), 
        It will ignore general earnings in the Sum

        --------------
        Exception Handling Should Be Added - 2 Feb, 2022.
        -------------

        :param ignore_category: The category earnings that shouldn't add to the Sum.
        :type ignore_category: str
        :raises Exception: Users or Categories Not Found In Table Earnings.
        :return: Individual User Earnings values in the form of dict.
        :rtype: dict
        '''

        cursor = self.connection.cursor()
        Month = datetime.today().month

        # Fetching User Names From Database
        Query_For_Retrieval = "SELECT DISTINCT(a.User) as Name FROM Earnings as a"
        try:
            cursor.execute(Query_For_Retrieval)

        except sqlite3.Error as e:
            print(f"Class: Earnings_V2, Function: individual_earnings_info, Error: {e}")

        else:
            result = cursor.fetchall()
            People_Names = [i['Name'] for i in result]

        # Fetching Categories Other Than Srinu Given From Database
        Query_For_Category = "SELECT DISTINCT(a.Category) as Category FROM Earnings as a"

        try:
            cursor.execute(Query_For_Category)

        except sqlite3.Error as e:
            print(f"Class: Earnings_V2, Function: individual_earnings_info, Error: {e}")

        else:
            result = cursor.fetchall()
            Category_Names = [i['Category'] for i in result if i['Category'] != ignore_category]

        if People_Names == [] or Category_Names == []:
            raise Exception(f"Class: Earnings_V2, Function: individual_earnings_info, Error: No Users in Database or No Categories Other Than '{ignore_category}' in the Database. Please Check Your Database")

        else:
            # Categories That Should Be Included
            values = {}
            Query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.User in (?) and m2.Category in (?)"
            for name in People_Names:

                sum = 0
                try:
                    for category in Category_Names:
                        cursor.execute(Query, (Month, name, category))
                        result = cursor.fetchone()
                        if result['Sum'] is None:
                            sum += 0
                        else:
                            sum += int(result['Sum'])
                except Exception as e:
                    print(f"Class: Earnings_V2, Function: individual_earnings_info, Error: {e}")
                    break
                else:
                    values[name] = sum

            if len(values) != len(People_Names):
                    print("Please Resolve The Above Error!!. This Function Doesn't Returned Any Output")
            else:
                return values


    def block_for_general_category(self):
        '''
        Returns Current Month individual General Category Sum Value 
        By default The 'Srinu Given' Category is Used in the code.
        We need to Change the code if we want to add list of categories

        :return: General Category Sum Value
        :rtype: int
        '''
        
        cursor = self.connection.cursor()
        Month = datetime.today().month
        try:
            Query = "select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.Category in (?)"
            cursor.execute(Query, (Month, 'Srinu Given'))

        except sqlite3.Error as e:
            print(f'Class: Earnings_V2, Function: block_srinu_given, Error: {e}')

        else:
            result = cursor.fetchone()
            if result['Sum'] is None:
                earnings_value = 0
            else:
                earnings_value = int(result['Sum'])
            return earnings_value

    def plot_person_wise_earnings(self, ignore_category="Srinu Given"):
        '''
        This is Modified Method in Parent Class: Earnings

        Returns current month individual user value percentage to plot donut chart.
        This function calculates only individual earnings like (Personal, Salary, Crypto etc.), 
        It will ignore general earnings for the percentage. 

        --------------
        Exception Handling Should Be Added - 6 Feb, 2022.
        -------------

        :param ignore_category: The category earnings that shouldn't add to the Sum, defaults to "Srinu Given"
        :type ignore_category: str, optional
        :raises Exception: Users or Categories Not Found In Table Earnings.
        :return: Individual Category Earnings Percentages, Category Names (percents, category_names)
        :rtype: (list, list)
        '''
        cursor = self.connection.cursor()
        Month = datetime.today().month

        # Fetching User Names From Database
        Query_For_Retrieval = "SELECT DISTINCT(a.User) as Name FROM Earnings as a"
        try:
            cursor.execute(Query_For_Retrieval)
        except sqlite3.Error as e:
            print(f"Class: Earnings_V2, Function: plot_person_wise_earnings, Error: {e}")
        else:
            result = cursor.fetchall()
            People_Names = [i['Name'] for i in result]

        # Fetching Categories Other Than Srinu Given From Database
        Query_For_Category = "SELECT DISTINCT(a.Category) as Category FROM Earnings as a"
        try:
            cursor.execute(Query_For_Category)
        except sqlite3.Error as e:
            print(f"Class: Earnings_V2, Function: plot_person_wise_earnings, Error: {e}")
        else:
            result = cursor.fetchall()
            Category_Names = [i['Category'] for i in result if i['Category'] != ignore_category]

        if People_Names == [] or Category_Names == []:
            raise Exception(f"Class: Earnings_V2, Function: plot_person_wise_earnings, Error: No Users in Database or No Categories Other Than '{ignore_category}' in the Database. Please Check Your Database")
        else:
            # Categories That Should Be Included
            values = []
            Query = "select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.User in (?) and m2.Category in (?)"
            for name in People_Names:
                s = 0
                try:
                    for category in Category_Names:
                        cursor.execute(Query, (Month, name, category))
                        result = cursor.fetchone()
                        if result['Sum'] is None:
                            s += 0
                        else:
                            s = int(result['Sum'])
                except Exception as e:
                    print(f"Class: Earnings_V2, Function: plot_person_wise_earnings, Error: {e}")
                    break
                else:
                    values.append(s)

            if len(values) != len(People_Names):
                    print("Please Resolve The Above Error!!. This Function Doesn't Returned Any Output")

            elif sum(values) == 0:
                # Log That this months Earnings are empty
                return values, People_Names

            else:
                total_sum = sum(values)
                percents = [int(i/total_sum * 100) for i in values]
                return percents, People_Names


if __name__ == "__main__":
    e = Earnings_V2("main_monitor.db")
    """
    Need To Change Plot_Person_Earnings Method too. That Method is Not Displaying Correctly.
    """
    # print(e.db_path)
    # print(e.block_for_general_category())
    # print(e.individual_earnings_info())
    # help(e)
    print(e.plot_person_wise_earnings())