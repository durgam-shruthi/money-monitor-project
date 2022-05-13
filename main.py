from flask import Flask, request, render_template
import sqlite3 as sql
from datetime import datetime, date
from app.crypto.crypto import Crypto
from app.categories.online import OnlineShopping
from app.categories.food import Food
from app.categories.home import Home
from app.categories.recharge import Recharge
from app.categories.health import Health 
from app.categories.festival import Festival
from app.categories.other import Other
from app.earnings.earnings_v2 import Earnings_V2
from app.payments.payment import Payment

app = Flask(__name__)

"""
    Need to add Previous Savings two functionalites. 
"""

def earnings_and_savings(earnings, savings, months, Month):
    a = [['Month', 'Earnings', 'Savings']]
    if Month in [1,2,3,4,5]:
        for i in range(5):
            a.append([months[i], earnings[i], savings[i]])
    else:
        for i in range(Month-5, Month):
            a.append([months[i], earnings[i], savings[i]])
    return a

# Dashboard
@app.route("/", methods=['GET', 'POST'])
def main():
    # INSERTING INFO INTO DATABASE (4 FORMS)
    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'form1':

            Bill = request.form['Bill']
            Holder_Name = request.form['Holder_Name']
            Category = request.form['Category']
            Payment_Mode = request.form['Payment_Mode']
            Amount = request.form['Amount']
            User = request.form['User']
            Date = date.today()
         
            with sql.connect("main_monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO amount_spend (Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) VALUES (?,?,?,?,?,?,?)",(Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) )
            
                con.commit()

        # Earnings Info
        elif form_name == 'form2':
            Amount = request.form['Amount']
            Category = request.form['Category']
            User = request.form['User']
            Amount_Form = request.form['amount_form']
            Date = date.today()

            with sql.connect("main_monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Earnings (Date, User, Category, Amount, Amount_Form) VALUES (?,?,?,?, ?)",(Date, User, Category, Amount, Amount_Form) )
            
                con.commit()       

        # Previous Savings Expenditure
        elif form_name == 'form3':
            Bill = request.form['Bill']
            Holder_Name = request.form['Holder_Name']
            Category = request.form['Category']
            Payment_Mode = request.form['Payment_Mode']
            Amount = request.form['Amount']
            User = request.form['User']
            Date = request.form['Date']
            Savings_Date = Date
         
            # Inserting into Previous Savings Table
            with sql.connect("main_monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO previous_savings (Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) VALUES (?,?,?,?,?,?,?)",(Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) )
            
                con.commit()

        # Dedicated Savings Information
        # Inserting Information Into Table
        elif form_name == 'form4':
            Amount = request.form['Amount']
            Product_Name = request.form['Product_Name']
            User = request.form['User']
            Amount_Form = request.form['Amount_Form']
            Date = date.today()
            print(Product_Name)
            with sql.connect("main_monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO dedicated_savings (Date, Product_Name, User, Amount_Form, Amount) VALUES (?,?,?,?,?)",(Date, Product_Name, User, Amount_Form, Amount) )
            
                con.commit()
       
        con.close()

    # Retrieving Information From tables
    con = sql.connect("main_monitor.db")
    con.row_factory = sql.Row

    # TODAY GENERAL INFO
    Day = datetime.today().day
    Date = datetime.now().strftime("%d %b %Y")
    Month = datetime.today().month
    Year = datetime.today().year

    # EXPENDITURE TABLE -- LAST BLOCK
    cur = con.cursor()
    cur.execute("SELECT * FROM amount_spend as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC  LIMIT 10 ; ")
    rows = cur.fetchall()


    # __________________________MONTHLY SAVINGS TABLE RECORDS GENERATION __________________________________

    Categories = ['Online Shopping', 'Food', 'Home Maintanence', 'Digital Recharge', 'Health Maintenance', 'Festival Expenditure', 'Others']
    table = con.cursor()
    check = con.cursor()
    insert = con.cursor()
    update = con.cursor()

    for i in Categories:
        # Check Whether this month & Category is there in amount spend
        check.execute("SELECT *, cast(substr(CAST(date as TEXT), 6, 2) as INT) as Month,  cast (substr(CAST(date as TEXT), 1, 4) as INT) as Year from amount_spend WHERE Month  = ? and Category = ? and Year = ?",(Month, i, Year))
        count = check.fetchall()
        # If Category is there in amount spend
        if len(count) > 0:

            # Getting Sum of Category Amount From Amount_spend
            table.execute("SELECT Sum(m1.Amount) as Amount FROM (Select *, cast (substr(CAST(date as TEXT), 6, 2) as INT) as Month,  cast (substr(CAST(date as TEXT), 1, 4) as INT) as Year from amount_spend WHERE Month  = ? and Year = ?) as m1 where m1.Category = ?",(Month,Year, i))
            record = table.fetchall()
            Amount = record[0]['Amount']

            # Check whether month, year and category there in monthly_data
            check1 = con.cursor()
            check1.execute("SELECT * from monthly_data WHERE Month  = ? and Category = ? and Year = ?",(Month, i, Year))
            count1 = check1.fetchall()

            # If month, year and category there in monthly_data is present
            if len(count1) > 0:
                update.execute("UPDATE monthly_data SET Amount = ? WHERE Month = ? AND Year = ? and Category = ?",(Amount, Month, Year, i))
                con.commit()
            # If not there
            else:
                insert.execute("INSERT INTO monthly_data (Month, Year, Category, Amount) VALUES (?,?,?,?);",
                        (Month, Year, i, Amount))
                con.commit()
        # If no record in Amount Spend
        else:
            # Check if Category with certain amount Is present
            check2 = con.cursor()
            check2.execute("SELECT * from monthly_data WHERE Month  = ? and Category = ? and Year = ?",(Month, i, Year))
            count2 = check2.fetchall()
            # IF There 
            if len(count2) > 0:
                # if Amount is > 1
                if count2[0]['Amount'] > 1:
                    update.execute("UPDATE monthly_data SET Amount = ? WHERE Month = ? AND Year = ? and Category = ?",(1, Month, Year, i))
                    con.commit()
                # if Amount is < 1
                else:
                    continue
            # if not there create new record with rupees 1
            else:
                insert.execute("INSERT INTO monthly_data (Month, Year, Category, Amount) VALUES (?,?,?,?);",
                            (Month, Year, i, int(1)))
                con.commit()


    # __________________________________ CATEGORY WISE EXPENDITURE TABLE __________________________________

    t3 = con.cursor()

    # CONDITION FOR JANUARY MONTH
    # Problem - What IF we have no record of Previous Months
    # Solution - Record with 1 RS for each record is sufficient

    # __________________________________ ONCE CHECK IT IN JANUARY, 2022 __________________________________

    if Month == 1:
        t3.execute("SELECT m1.Category, m1.Amount, m2.Amount as Amount_Previous, CAST(((m1.Amount - m2.Amount) / m2.Amount * 100) as INT) as Percentage FROM (SELECT Category, Amount  FROM monthly_data  WHERE Month = ? and Year = ? ) as m1 JOIN (SELECT Category , Amount FROM monthly_data  WHERE Month = ? and Year = ? ) as m2 ON (m1.Category = m2.Category);",
                (Month, Year, 12, Year-1))

    # FOR ALL OTHER MONTHS
    else:
        t3.execute("SELECT m1.Category, m1.Amount, m2.Amount as Amount_Previous, CAST(((m1.Amount - m2.Amount) / m2.Amount * 100) as INT) as Percentage FROM (SELECT Category, Amount  FROM monthly_data  WHERE Month = ? and Year = ? ) as m1 JOIN (SELECT Category , Amount FROM monthly_data  WHERE Month = ? and Year = ?) as m2 ON (m1.Category = m2.Category);",
                (Month, Year, Month-1, Year))
    categories = t3.fetchall()

    # __________________________________ ONCE CHECK IT IN JANUARY, 2022 __________________________________


    # __________________________________ FOUR INFO's ________________________________________

    # Amount Spend Today
    t_amount = con.cursor()
    t_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as day,CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.day in (?) and m2.Month in (?) and m2.Year in (?) ", (9, 2, Day, Month, Year))
    today_money = t_amount.fetchall()
    if [i['Sum'] for i in today_money][0] is None:
        today_amount = 0
    else:
        today_amount = int([i['Sum'] for i in today_money][0])

    # Monthly Spend amount
    m_amount = con.cursor()
    m_amount.execute("select sum(m2.Amount) as Sum, count(m2.Amount) as Count from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, Month, Year))
    month_m = m_amount.fetchall()
    if [i['Sum'] for i in month_m][0] is None:
        month_money = 0
    else:
        month_money = int([i['Sum'] for i in month_m][0])
    
    # Monthly Transaction Count
    if [i['Count'] for i in month_m][0] is None:
        transaction_count = 0
    else:
        transaction_count = [i['Count'] for i in month_m][0]

    # Last Month Amount Spend (Same as Category Wise Expenditure Table)
    l_amount = con.cursor()
    # __________________________________ ONCE CHECK IT IN JANUARY, 2022 __________________________________
    
    if Month == 1:
        l_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, 12, Year-1))
    else:
        l_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, Month-1, Year))
    month_l = l_amount.fetchall()
    if [i['Sum'] for i in month_l][0] is None:
        last_month_money = 0
    else:
        last_month_money = int([i['Sum'] for i in month_l][0])

    # __________________________________ ONCE CHECK IT IN JANUARY, 2022 __________________________________

    # Expenditure Percentage
    if last_month_money == 0:
        Expenditure = 0
    else:
        Expenditure = int(((month_money - last_month_money) / last_month_money) * 100)

    # Monthly Earnings
    m_earning = con.cursor()
    m_earning.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, Month, Year))
    month_earning = m_earning.fetchall()
    if [i['Sum'] for i in month_earning][0] is None:
        month_earning = 0
    else:
        month_earning= int([i['Sum'] for i in month_earning][0])

    # Monthly Savings
    month_saving = int(month_earning - month_money)

    # __________________________________ MONTLY SPEND REPORT ________________________________________

    d_amount = con.cursor()
    day_data = []
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Year in (?)", (Month, i, Year))
        d_spend = d_amount.fetchall()
        if [i['Sum'] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i['Sum'] for i in d_spend][0])
        day_data.append(day_spend)

    # Day Wise Amount Spend
    day_values = day_data

    # __________________________________ YEARLY REPORT ________________________________________

    # Identify Previous Savings Expenditure Info To Amount Spend Info
    P_Query = "select sum(m2.Amount) as Previous_Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month,CAST(substr(m1.'Date', 1, 4) as INT) as Year from previous_savings as m1) as m2 Where m2.Month in (?) and m2.Year in (?) "
    y_amount = con.cursor()
    y_pe_amount = con.cursor()
    year_data = []
    for i in range(1, 13):
        y_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month,CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, i, Year))
        y_pe_amount.execute(P_Query, (6, 2, i, Year))
        y_spend = y_amount.fetchall()
        y_pe_spend = y_pe_amount.fetchone()

        # For Previous Savings Expenditure
        if y_pe_spend['Previous_Sum'] is None:
            pe_spend = 0
        else:
            pe_spend = y_pe_spend['Previous_Sum']

        # For Monthly Spent Expenditure
        if [i['Sum'] for i in y_spend][0] is None:
            year_spend = 0
        else:
            year_spend = int([i['Sum'] for i in y_spend][0])
        year_data.append(year_spend+pe_spend)

    # Yearly Amount Spend Values
    values = year_data
    # Taken earing's and saving's values from earnings and savings report

    # __________________________________ EARNING'S AND SAVING'S REPORT ________________________________________

    e_report = con.cursor()
    year_e_values = []
    months = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul',
        8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    Months = []
    
    # Yearly Earned Amount
    for i in range(1, 13):
        e_report.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, i, Year))
        e_month = e_report.fetchall()

        if [j['Sum'] for j in e_month][0] is None:
            earn_month = 0
            Months.append(months[i])
        else:
            earn_month = int([j['Sum'] for j in e_month][0])
            Months.append(months[i])
        year_e_values.append(earn_month)

    e_values = year_e_values
    a_values = year_data

    # Yearly Savings Values
    s_values = []
    for i in range(12):
        if e_values[i] - a_values[i] < 0:
            s_values.append(0)
        else:
            s_values.append(e_values[i] - a_values[i])

    # Random S_Values
    # s_values[2] = 1000
    # s_values[3] = 1000
    # s_values[4] = 1000

    # Earnings Percentage
    if e_values[Month-2] == 0:
        e_percentage = 0
    else:
        e_percentage = int((e_values[Month-1] - e_values[Month-2]) / e_values[Month-2] * 100)
    
    # Savings Percentage
    if s_values[Month-2] == 0:
        s_percentage = 0
    else:
        s_percentage = int((s_values[Month-1] - s_values[Month-2]) / s_values[Month-2] * 100)

    # Using earnings & savings function to get last 5 months data
    e_and_savings = earnings_and_savings(earnings=e_values, savings=s_values, months=Months, Month=Month)




    # __________________________________ VERSION 2 ________________________________________
    
    # __________________________________ SAVING'S INFO STORING ________________________________________

    savings = con.cursor()
    s_cursor = con.cursor()
    for i in range(12):
        # Check if savings record is there
        savings.execute("Select Count(*) as count from savings where Month = ? and Year = ?", 
                (i+1, Year))
        count = savings.fetchall()
        # if that month record not present
        if [j['count'] for j in count][0] == 0:

            # Insert that months record 
            s_cursor.execute("INSERT INTO savings (Month, Year, Amount) VALUES (?,?,?);",
                    (i+1, Year, s_values[i]))
            con.commit()

        # if that month record is present
        else:
            # Check If the DB amount and s_values amount of that month is same
            db_amt = savings.execute("Select Amount from savings where Month = ? and Year = ?", (i+1, Year))
            db_amount = db_amt.fetchall()[0]['Amount']
            # If same then continue
            if db_amount == s_values[i]:
                continue
            else:
                # Update that months record 
                s_cursor.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(s_values[i], i+1, Year))
                con.commit()


    # Previous Savings
    previous_savings = sum(s_values) - month_saving
    print(f"previous_savings: {previous_savings}")


    # __________________________________ DEDICATED SAVINGS BLOCK ________________________________________

    # Passing Product Names Into Dedicated Savings Form
    p_names = con.cursor()
    p_names.execute("SELECT DISTINCT(Product_Name) from target")
    product_n = p_names.fetchall()
    if len([i['Product_Name'] for i in product_n]) == 0:
        product_n = ["No Targets"]
    else:
        product_n = [i['Product_Name'] for i in product_n]

    print(product_n)

    # __________________________________ UPDATING SAVING'S AND CALCULATING NEW PREVIOUS SAVING'S __________________________

    # Taking Sum Of All Dedicated Savings Amount From Database

    l_ds = con.cursor()
    l_ds.execute("SELECT SUM(Amount) as 'Sum' FROM dedicated_savings as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC; ")
    latest_ds = l_ds.fetchall()[0]
    Amount = latest_ds['Sum']
    print(f"Latest Amount: {Amount}")

    # Updating Saving Values
    u_ps = con.cursor()
    u_ms = con.cursor()
    u_savings = con.cursor()

    # Retriving Savings Values From Table
    s = con.cursor()
    s.execute("Select * from savings")
    sav_values = s.fetchall()
    savings_values = []

    # If Total Sum is Null
    if Amount is None:
        Amount = 0
    
    # SUM Of Dedicated Savings
    dedicated_savings = int(Amount)

    # If Total Sum is > than Previous Savings and < Sum of Previous and Monthly Savings
    if Amount > previous_savings:

        Remaining_Amount = Amount - previous_savings

        # For Previous Savings
        for i in sav_values:
            # Excluding this months and future months records
            if i['Month'] >= Month and i['Year'] == Year:
                continue
            else:
                u_ps.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(0, i['Month'], i['Year']))
                con.commit()

        # For Monthly Savings
        month_saving = int(month_saving - Remaining_Amount)
        print(month_saving)
        u_ms.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(month_saving, Month, Year))
        con.commit()

        previous_savings = int(0)

    # if Total Sum is < Previous Savings
    
    else:
        for i in sav_values:
            # Excluding this months and future months records
            if i['Month'] >= Month and i['Year'] == Year:
                continue
            else:
                
                if Amount > i['Amount']:
                    Amount = Amount - i['Amount']
                    u_savings.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(0, i['Month'], i['Year']))
                    con.commit()
                    savings_values.append(0)
                elif Amount <= i['Amount']:
                    u_savings.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(i['Amount'] - Amount, i['Month'], i['Year']))
                    con.commit()
                    savings_values.append(i['Amount'] - Amount)
                    Amount = 0
                    

    print(savings_values)
    previous_savings = sum(savings_values)

    print(f"previous_savings After: {previous_savings}")

    return render_template('index.html', rows=rows, categories=categories, today_amount=today_amount, Date=Date,
                            month_money=month_money, month_earning=month_earning, transaction_count=transaction_count, Expenditure=Expenditure, 
                            values=values, day_values=day_values, e_values=e_values,  e_percentage=e_percentage,  Product_Names=product_n, 
                            previous_savings=int(previous_savings), month_saving=month_saving, s_values=s_values, e_and_savings=e_and_savings, s_percentage=s_percentage,
                            dedicated_savings=int(dedicated_savings))
    

@app.route("/crypto", methods=['GET', 'POST'])
def crypto():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Crypto object
    # Currently using Version 1 Method: 14 Feb, 2022
    crypto = Crypto(db_path="main_monitor.db")
    # Retrieving values for four blocks
    today_crypto_earn, month_crypto_count, month_crypto_earn, year_crypto_earn = crypto.get_four_blocks()
    # Retrieving Current Month Daily Crypto Earnings Values
    month_values = crypto.plot_current_month_crypto_earnings()
    # Latest 10 Crypto Earnings
    rows = crypto.get_latest_ten_earnings()


    return render_template('Cryptocurrency.html', Date=Date, today_crypto_earn=today_crypto_earn, 
                            month_crypto_count=month_crypto_count, month_crypto_earn=month_crypto_earn, year_crypto_earn=year_crypto_earn,
                            month_values=month_values, rows=rows)


@app.route("/online", methods=['GET'])
def online():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating OnlineShopping object
    # Currently using Version 1 Method: 13 Feb, 2022
    online = OnlineShopping(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = online.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = online.get_latest_ten_spends()


    return render_template('Online.html', Date=Date, month_values=month_values, rows=rows)


@app.route("/food", methods=['GET'])
def food():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Food object
    # Currently using Version 1 Method: 13 Feb, 2022
    food = Food(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = food.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = food.get_latest_ten_spends()

    return render_template('Food.html', Date=Date, month_values=month_values, rows=rows)


@app.route("/home", methods=['GET'])
def home():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Home object
    # Currently using Version 1 Method: 13 Feb, 2022
    home = Home(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = home.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = home.get_latest_ten_spends()


    return render_template('Home.html', Date=Date, month_values=month_values, rows=rows)


@app.route("/recharge", methods=['GET'])
def recharge():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Recharge object
    # Currently using Version 1 Method: 13 Feb, 2022
    recharge = Recharge(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = recharge.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = recharge.get_latest_ten_spends()

    return render_template('Recharge.html', Date=Date, month_values=month_values, rows=rows)


@app.route("/health", methods=['GET'])
def health():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Health object
    # Currently using Version 1 Method: 13 Feb, 2022
    health = Health(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = health.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = health.get_latest_ten_spends()

    return render_template('Health.html', Date=Date, month_values=month_values,  rows=rows)


@app.route("/festival", methods=['GET'])
def festival():

    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Other object
    # Currently using Version 1 Method: 12 Feb, 2022
    festival = Festival(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = festival.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = festival.get_latest_ten_spends()

    return render_template('Festival.html', Date=Date, month_values=month_values, rows=rows)


@app.route("/other", methods=['GET'])
def other():
    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Other object
    # Currently using Version 1 Method: 12 Feb, 2022
    other = Other(db_path="main_monitor.db")
    # Current Month Daily Spent
    month_values = other.plot_current_month_daily_spend()
    # Latest 10 transactions
    rows = other.get_latest_ten_spends()

    return render_template('Others.html', Date=Date, month_values=month_values, rows=rows)


@app.route("/earning", methods=['GET'])
def earning():
    Date = datetime.now().strftime("%d %b %Y")
    # Instianting Earnings Object with Database Path
    # Currently using Version 2 Method: 2 Feb, 2022
    earning = Earnings_V2("main_monitor.db")
    # Display Individual Earnings Info (3 Blocks)
    earned_amount = earning.individual_earnings_info()
    # Srinu Given Category Block
    srinu_given_earnings = earning.block_for_general_category()
    # Plot Individual User Earnings
    percents, user_names = earning.plot_person_wise_earnings()
    # Plot Individual Category Earnings
    category_percents, category_names = earning.plot_category_wise_earnings()
    # Plot Monthy Earnings
    monthly_earnings = earning.plot_monthly_earnings()
    # Latest Earnings Upto 15 Rows
    rows = earning.display_table()

    return render_template("Earnings.html", Date=Date, earned_amount=earned_amount, srinu_given_earnings=srinu_given_earnings, percents=percents, labels=user_names ,
                            category_percents=category_percents, categories=category_names, 
                            monthly_earnings=monthly_earnings, rows=rows)


@app.route("/payment", methods=['GET'])
def payment():
    Date = datetime.now().strftime("%d %b %Y")
    # Instantiating Payment object
    # Currently using Version 1 Method: 12 Feb, 2022
    payment = Payment(db_path="main_monitor.db")
    # Retrieving values for four blocks
    month_cash_spend, month_credit_spend, month_debit_spend, month_upi_spend = payment.get_four_blocks()
    # Retrieving percentage values for donut chart
    percents = payment.plot_amount_spent_payment_types()


    return render_template('Payment.html', Date=Date, month_cash_spend=month_cash_spend, 
                            month_credit_spend=month_credit_spend, month_debit_spend=month_debit_spend, month_upi_spend=month_upi_spend, percents=percents)

# Version 2
# Adding target API
@app.route("/target", methods=['GET', 'POST'])
def target():

    Date = datetime.now().strftime("%d %b %Y")

    if request.method == 'POST':
        form_name = request.form['form-name']
        if form_name == 'target-form':

            Product_name = request.form['Product_name']
            Product_price = request.form['Product_price']
            Product_link = request.form['Product_link']
            Upload_file = request.form['img[]']
            folder_path = 'static/Target_Images/'
            Upload_file_path = folder_path + Upload_file
            Date = date.today()

            with sql.connect("main_monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO target (Date, Product_Name, Product_Link, File_Path, Target_Price, Savings_Duration) VALUES (?,?,?,?,?,?)",(Date, Product_name, Product_link, Upload_file_path, Product_price, 0) )
            
                con.commit()
                msg = "Record successfully added from Target-Form"
                print(msg)

    con = sql.connect("main_monitor.db")
    con.row_factory = sql.Row
    targets = con.cursor()
    targets.execute("SELECT * FROM target as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC  LIMIT 10 ; ")
    rows = targets.fetchall()
    values = []
    if len(rows) < 2:
        values.append(rows)
    elif len(rows) % 2 == 0:
        for i in range(0, len(rows), 2):
            values.append([rows[i], rows[i+1]])
    else:
        for i in range(0, len(rows)-1, 2):
            values.append([rows[i], rows[i+1]])
        values.append([rows[len(rows)-1]])

    print(values)
    # Current Price from Dedicated Savings table
    # Should Be In the Form of Dict
    Current_prices = {'TV': 0, 'Plot':0}

    # Percentages
    # Target Price
    target_price = {}
    for row in rows:
        target_price[row['Product_Name']] = row['Target_Price']

    percentages = {}
    for i in Current_prices:
        percentages[i] = int((Current_prices[i] / target_price[i]) * 100)

    print(percentages)
    return render_template('Targets.html', Date=Date, values=values, rows=rows, Current_prices=Current_prices, percentages=percentages)

if __name__ == "__main__":
    app.run(debug=True)