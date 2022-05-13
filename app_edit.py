from flask import Flask, request, render_template
from flask import Response
import sqlite3 as sql
import requests, json
from datetime import datetime, date

app = Flask(__name__)

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
    # Taking Forms Information 
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
         
            with sql.connect("monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO amount_spend (Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) VALUES (?,?,?,?,?,?,?)",(Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) )
            
                con.commit()
                msg = "Record successfully added from Form 1"
                print(msg)

        # Earnings Info
        elif form_name == 'form2':
            Amount = request.form['Amount']
            Category = request.form['Category']
            User = request.form['User']
            Amount_Form = request.form['amount_form']
            Date = date.today()

            with sql.connect("monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Earnings (Date, User, Category, Amount, Amount_Form) VALUES (?,?,?,?, ?)",(Date, User, Category, Amount, Amount_Form) )
            
                con.commit()
                msg = "Record successfully added from Form 2"
                print(msg)           

                form_name = request.form['form-name']

        # Previous Savings Expenditure
        elif form_name == 'form3':
            Bill = request.form['Bill']
            Holder_Name = request.form['Holder_Name']
            Category = request.form['Category']
            Payment_Mode = request.form['Payment_Mode']
            Amount = request.form['Amount']
            User = request.form['User']
            Date = request.form['Date']
         
            with sql.connect("monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO amount_spend (Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) VALUES (?,?,?,?,?,?,?)",(Date, User, Bill, Holder_Name, Category, Payment_Mode, Amount) )
            
                con.commit()
                msg = "Record successfully added from Form 3"
                print(msg)

        # Dedicated Savings Information
        # Inserting Information Into Table
        elif form_name == 'form4':
            Amount = request.form['Amount']
            Product_Name = request.form['Product_Name']
            User = request.form['User']
            Amount_Form = request.form['Amount_Form']
            Date = date.today()
            print(Product_Name)
            with sql.connect("monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO dedicated_savings (Date, Product_Name, User, Amount_Form, Amount) VALUES (?,?,?,?,?)",(Date, Product_Name, User, Amount_Form, Amount) )
            
                con.commit()
                msg = "Record successfully added from Form 4"
                print(msg)
        con.close()

    # Retrieving Information From tables
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    Month = datetime.today().month
    Day = datetime.today().day
    Date = datetime.now().strftime("%d %b %Y")
    Year = datetime.today().year
    cur = con.cursor()
    t3 = con.cursor()
    table = con.cursor()
    check = con.cursor()
    insert = con.cursor()
    update = con.cursor()
    # Expenditure Table -- LAST BLOCK
    cur.execute("SELECT * FROM amount_spend as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC  LIMIT 10 ; ")

    # Table 3 Records Generation - FOR MONTHLY SAVINGS
    for i in ['Online Shopping', 'Food', 'Home Maintanence', 'Digital Recharge', 'Health Maintenance', 'Festival Expenditure', 'Others']:
        table.execute("SELECT m1.Month, m1.Year, m1.Category, Sum(m1.Amount) as Amount FROM (Select *, cast (substr(CAST(date as TEXT), 6, 2) as INT) as Month,  cast (substr(CAST(date as TEXT), 1, 4) as INT) as Year from amount_spend WHERE Month  = ?) as m1 where m1.Category = ?",(Month, i))
        record = table.fetchall()
        values = []
        for i in record:
            values.append(i['Month'])
            values.append(i['Year'])
            values.append(i['Category'])
            values.append(i['Amount'])
        
        check.execute("Select Count(*) as count from monthly_data WHERE EXISTS (select * from monthly_data where Month = ? and Year = ? and Category = ?)", 
                    (values[0], values[1], values[2]))
        count = check.fetchall()
        if [i['count'] for i in count][0] == 0:
            if values[0] is None and values[2] is None:
                continue
            else:
                insert.execute("INSERT INTO monthly_data (Month, Year, Category, Amount) VALUES (?,?,?,?);",
                        (values[0], values[1], values[2], values[3]))
                con.commit()
        else:
            update.execute("UPDATE monthly_data SET Amount = ? WHERE Month = ? AND Year = ? and Category = ?",(values[3], values[0], values[1], values[2]))
            con.commit()
 
    # Category Wise Table - TAKING RECORDS & CALCULATING PERCENTAGES
    # Need to CHeck how to add year here
    t3.execute("SELECT m1.Category, m1.Amount, m2.Amount as Amount_Previous, CAST(((m1.Amount - m2.Amount) / m2.Amount * 100) as INT) as Percentage FROM (SELECT Category, Amount  FROM monthly_data  WHERE Month = ? ) as m1 JOIN (SELECT Category , Amount FROM monthly_data  WHERE Month = ? ) as m2 ON (m1.Category = m2.Category);",
                (Month, Month-1))
    rows = cur.fetchall()
    categories = t3.fetchall()

    # Four Info's - FIRST 4 BLOCKS
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
    # Monthly Transaction 

    if [i['Count'] for i in month_m][0] is None:
        transaction_count = 0
    else:
        transaction_count = [i['Count'] for i in month_m][0]

    # Last Month Amount Spend
    l_amount = con.cursor()
    l_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month, CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, Month-1, Year))
    month_l = l_amount.fetchall()
    if [i['Sum'] for i in month_l][0] is None:
        last_month_money = 0
    else:
        last_month_money = int([i['Sum'] for i in month_l][0])
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

    # Yearly Report
    y_amount = con.cursor()
    year_data = []
    for i in range(1, 13):

        y_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', ?, ?) as INT) as Month,CAST(substr(m1.'Date', 1, 4) as INT) as Year from amount_spend as m1) as m2 Where m2.Month in (?) and m2.Year in (?) ", (6, 2, i, Year))
        y_spend = y_amount.fetchall()
        if [i['Sum'] for i in y_spend][0] is None:
            year_spend = 0
        else:
            year_spend = int([i['Sum'] for i in y_spend][0])
        year_data.append(year_spend)

    values = year_data

    # Monthly Report
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

    day_values = day_data

    # Earning's and Saving's Report
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

    s_values = []
    for i in range(12):
        if e_values[i] - a_values[i] < 0:
            s_values.append(0)
        else:
            s_values.append(e_values[i] - a_values[i])

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

    # This should link with Database
    e_and_savings = earnings_and_savings(earnings=e_values, savings=s_values, months=Months, Month=Month)

    # Version 2 Addings

    # Storing Savings Information
    savings = con.cursor()
    s_insert = con.cursor()
    s_update = con.cursor()
    for i in range(12):
        savings.execute("Select Count(*) as count from savings WHERE EXISTS (select * from savings where Month = ? and Year = ?)", 
                (i+1, Year))
        count = savings.fetchall()
        if [j['count'] for j in count][0] == 0:
            if (i+1) is None:
                continue
            else:
                s_insert.execute("INSERT INTO savings (Month, Year, Amount) VALUES (?,?,?);",
                        (i+1, Year, s_values[i]))
                con.commit()
        else:
            s_update.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(s_values[i], i+1, Year))
            con.commit()

    # Previous Savings

    previous_savings = sum(s_values) - month_saving
    print(f"previous_savings: {previous_savings}")
    # Dedicated Savings
    # Passing Product Names
    p_names = con.cursor()
    p_names.execute("SELECT DISTINCT(Product_Name) from target")
    product_n = p_names.fetchall()
    if len([i['Product_Name'] for i in product_n]) == 0:
        product_n = ["No Targets"]
    else:
        product_n = [i['Product_Name'] for i in product_n]

    print(product_n)

    # Latest Dedicated Savings Amount
    l_ds = con.cursor()
    l_ds.execute("SELECT SUM(Amount) as 'Sum' FROM dedicated_savings as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC; ")
    latest_ds = l_ds.fetchall()[0]
    Amount = latest_ds['Sum']
    print(f"Latest Amount: {Amount}")
    # Updating Saving Values
    s = con.cursor()
    s.execute("Select * from savings")
    u_ps = con.cursor()
    u_ms = con.cursor()
    u_savings = con.cursor()
    sav_values = s.fetchall()
    savings_values = []

    if Amount is None:
        Amount = 0
    
    if Amount > previous_savings:
        Remaining_Amount = Amount - previous_savings
        # For Previous Savings
        for i in sav_values:
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

    # if Amount < Previous Savings
    
    else:
        for i in sav_values:
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

    # SUM Of Dedicated Savings

    d_savings = con.cursor()
    d_savings.execute("Select Sum(Amount) as 'Sum' from dedicated_savings")
    ded_savings = d_savings.fetchall()[0]
    if ded_savings['Sum'] is None:
        dedicated_savings = 0
    else:
        dedicated_savings = int(ded_savings['Sum'])

    # Dedicting Amount for Previous Savings Expenditure
    exp = con.cursor()
    exp.execute("SELECT Amount FROM amount_spend as a WHERE 'S No'  > 0 ORDER BY a.'S No' DESC LIMIT 1; ")
    expenditure = exp.fetchall()[0]
    exp_amount = expenditure['Amount']

    if exp_amount is None:
        exp_amount = 0

    svalues = []
    # Importing Savings Values
    a = con.cursor()
    a.execute("Select * from savings")
    b = a.fetchall()

    # Updating Savings Values
    # for i in b:
    #     if i['Month'] >= Month and i['Year'] == Year:
    #         continue
    #     else:

    #         if exp_amount > i['Amount']:
    #             exp_amount = exp_amount - i['Amount']
    #             u_savings.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(0, i['Month'], i['Year']))
    #             con.commit()
    #             svalues.append(0)
    #         elif exp_amount <= i['Amount']:
    #             u_savings.execute("UPDATE savings SET Amount = ? WHERE Month = ? AND Year = ? ",(i['Amount'] - exp_amount, i['Month'], i['Year']))
    #             con.commit()
    #             svalues.append(i['Amount'] - exp_amount)
    #             exp_amount = 0
 
    # Calculating Final Savings Value

    # print(svalues)
    # previous_savings = sum(svalues)


    return render_template('index.html', rows=rows, categories=categories, today_amount=today_amount, Date=Date,
                            month_money=month_money, month_earning=month_earning, transaction_count=transaction_count, Expenditure=Expenditure, 
                            values=values, day_values=day_values, e_values=e_values,  e_percentage=e_percentage,  Product_Names=product_n, 
                            previous_savings=int(previous_savings), month_saving=month_saving, s_values=s_values, e_and_savings=e_and_savings, s_percentage=s_percentage,
                            dedicated_savings=int(dedicated_savings))
    



@app.route("/crypto", methods=['GET', 'POST'])
def crypto():
    # Four Info's

    # 1. Today Earnings
    Date = datetime.now().strftime("%d %b %Y")
    day = datetime.today().day
    month = datetime.today().month
    con = sql.connect("monitor.db")
    t_earn = con.cursor()
    t_earn.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Crypto Earning')", (month, day))
    today_earn = t_earn.fetchall()
    if ([i[0] for i in today_earn][0]) is None:
        today_crypto_earn = 0
    else:
        today_crypto_earn = int([i[0] for i in today_earn][0])
    print("Crypto Page Starts ---")
    print(today_crypto_earn)

    # 2. Month total Crypto Transactions
    c_earn = con.cursor()
    c_earn.execute("select count(m2.Amount) as Count from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Category in (?) and m2.Month in (?)", ('Crypto Earning',month))
    count_earn = c_earn.fetchall()
    if [i[0] for i in count_earn][0] is None:
        month_crypto_count = 0
    else:
        month_crypto_count = [i[0] for i in count_earn][0]
    
    # 3. Month Crypto Earnings
    m_earn = con.cursor()
    m_earn.execute("select SUM(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Category in (?) and m2.Month in (?)", ('Crypto Earning',month))
    m_earnings = m_earn.fetchall()
    if [i[0] for i in m_earnings][0] is None:
        month_crypto_earn = 0
    else:
        month_crypto_earn = int([i[0] for i in m_earnings][0])
    
    # 4. Yearly Crypto Earnings
    year = datetime.today().year
    y_earn = con.cursor()
    y_earn.execute("select SUM(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 1, 4) as INT) as Year from Earnings as m1) as m2 Where m2.Category in (?) and m2.Year in (?)", ('Crypto Earning',year))
    y_earnings = y_earn.fetchall()
    if [i[0] for i in y_earnings][0] is None:
        year_crypto_earn = 0
    else:
        year_crypto_earn = int([i[0] for i in y_earnings][0])

    
    # Monthly Crypto Chart
    m_earnings = con.cursor()
    day_data = []
    for i in range(1, 32):
        m_earnings.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from Earnings as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in (?)", (month, i, 'Crypto Earning'))
        d_spend = m_earnings.fetchall()

        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Crypto Data

    c_data = con.cursor()
    c_data.execute("SELECT * FROM Earnings as a WHERE a.'S No'  > 0 and a.'Category' in ('Crypto Earning') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = c_data.fetchall()


    return render_template('Cryptocurrency.html',Date=Date, today_crypto_earn=today_crypto_earn, 
                            month_crypto_count=month_crypto_count, month_crypto_earn=month_crypto_earn, year_crypto_earn=year_crypto_earn,
                            month_values=month_values, rows=rows)

@app.route("/online", methods=['GET'])
def online():
    # Monthly Online Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Online Shopping')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Online Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Online Shopping') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()


    return render_template('Online.html', Date=Date, month_values=month_values, rows=rows)

@app.route("/food", methods=['GET'])
def food():

    # Monthly Food Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Food')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Food Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Food') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()

    return render_template('Food.html', Date=Date, month_values=month_values, rows=rows)

@app.route("/home", methods=['GET'])
def home():

    # Monthly Food Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Home Maintanence')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Food Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Home Maintanence') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()


    return render_template('Home.html', Date=Date, month_values=month_values, rows=rows)

@app.route("/recharge", methods=['GET'])
def recharge():
    # Monthly Food Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Digital Recharge')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Food Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Digital Recharge') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()

    return render_template('Recharge.html', Date=Date, month_values=month_values, rows=rows)

@app.route("/health", methods=['GET'])
def health():
    # Monthly Food Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Health Maintenance')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Food Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Health Maintenance') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()

    return render_template('Health.html', Date=Date, month_values=month_values,  rows=rows)

@app.route("/festival", methods=['GET'])
def festival():

    # Monthly Food Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Festival Expenditure')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Food Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Festival Expenditure') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()
    return render_template('Festival.html', Date=Date, month_values=month_values, rows=rows)

@app.route("/other", methods=['GET'])
def other():
    # Monthly Food Transactions
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    d_amount = con.cursor()
    day_data = []
    Month = datetime.today().month
    for i in range(1, 32):

        d_amount.execute("select sum(m2.Amount) as Sum from (select *, CAST(substr(m1.'Date', 9, 2) as INT) as day, CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?) and m2.day in (?) and m2.Category in ('Others')", (Month, i))
        d_spend = d_amount.fetchall()
        if [i[0] for i in d_spend][0] is None:
            day_spend = 0
        else:
            day_spend = int([i[0] for i in d_spend][0])
        day_data.append(day_spend)

    month_values = day_data

    # Latest Food Transactions

    o_data = con.cursor()
    o_data.execute("SELECT * FROM amount_spend as a WHERE a.'S No'  > 0 and a.'Category' in ('Others') ORDER BY a.'S No' DESC  LIMIT 10;")
    rows = o_data.fetchall()
    return render_template('Others.html', Date=Date, month_values=month_values, rows=rows)

@app.route("/payment", methods=['GET'])
def payment():
    Date = datetime.now().strftime("%d %b %Y")
    con = sql.connect("monitor.db")
    con.row_factory = sql.Row
    Month = datetime.today().month
    # Four Info's
    # 1. Monthly Cash Payments
    m_cash = con.cursor()
    m_cash.execute("select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?)  and m2.Payment_Mode in (?)", (Month, 'Cash'))
    m_cash_spend = m_cash.fetchall()
    if [i[0] for i in m_cash_spend][0] is None:
        month_cash_spend = 0
    else:
        month_cash_spend = int([i[0] for i in m_cash_spend][0])

    # 2. Monthly Credit Card
    m_credit = con.cursor()
    m_credit.execute("select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?)  and m2.Payment_Mode in (?)", (Month, 'Credit Card'))
    m_credit_spend = m_credit.fetchall()
    if [i[0] for i in m_credit_spend][0] is None:
        month_credit_spend = 0
    else:
        month_credit_spend = int([i[0] for i in m_credit_spend][0])

    # 3. Monthly Debit Card
    m_debit = con.cursor()
    m_debit.execute("select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?)  and m2.Payment_Mode in (?)", (Month, 'Debit Card'))
    m_debit_spend = m_debit.fetchall()
    if [i[0] for i in m_debit_spend][0] is None:
        month_debit_spend = 0
    else:
        month_debit_spend = int([i[0] for i in m_debit_spend][0])

    # 4. Monthly UPI
    m_upi = con.cursor()
    m_upi.execute("select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?)  and m2.Payment_Mode in (?, ?)", (Month, 'Phonpe UPI', 'Google Pay UPI'))
    m_upi_spend = m_upi.fetchall()
    if [i[0] for i in m_upi_spend][0] is None:
        month_upi_spend = 0
    else:
        month_upi_spend = int([i[0] for i in m_upi_spend][0])
    print(month_cash_spend, month_credit_spend, month_debit_spend, month_upi_spend)

    # Donut Chart
    # Calculating Phonepe UPI
    m_ppay = con.cursor()
    m_ppay.execute("select sum(m2.Amount) as Sum from (select *,  CAST(substr(m1.'Date', 6, 2) as INT) as Month from amount_spend as m1) as m2 Where m2.Month in (?)  and m2.Payment_Mode in (?)", (Month, 'Phonpe UPI'))
    m_ppay_spend = m_ppay.fetchall()
    if [i[0] for i in m_ppay_spend][0] is None:
        month_ppay_spend = 0
    else:
        month_ppay_spend = int([i[0] for i in m_ppay_spend][0])
    # Google Pay UPI
    month_gpay_spend = month_upi_spend - month_ppay_spend
    sum = month_cash_spend + month_credit_spend + month_debit_spend + month_upi_spend
    value = [month_cash_spend, month_credit_spend, month_debit_spend, month_ppay_spend, month_gpay_spend]
    if sum == 0:
        percents = []
    else:
        percents = [int(i/sum * 100) for i in value]
    print(percents)
    # 1. Bar Chart
    # 2. Bar Chart
    # 3. Bar Chart
    # 4. Bar Chart
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

            with sql.connect("monitor.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO target (Date, Product_Name, Product_Link, File_Path, Target_Price, Savings_Duration) VALUES (?,?,?,?,?,?)",(Date, Product_name, Product_link, Upload_file_path, Product_price, 0) )
            
                con.commit()
                msg = "Record successfully added from Target-Form"
                print(msg)

    con = sql.connect("monitor.db")
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
    app.run()