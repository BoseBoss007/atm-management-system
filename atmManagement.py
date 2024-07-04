from xml.dom.expatbuilder import parseFragmentString
import mysql.connector
import os
from datetime import datetime
import sys
hostValue = "localhost"
userValue = "root"
passwdValue = "8017"


def database():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue)
        cur = db.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS atm;")
        db.commit()
        cur.close()
        db.close()
        print("Database created sucessfully!!")

    except Exception as e:
        print("databse creation error", e)

# admin table creation


def admin():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue, database="atm")
        cur = db.cursor()
        cur.execute('''create table if not exists admindb(
            username varchar(50) default 'admin',
            password varchar(20) default 'admin')''')
        customer()
        cur.close()
        db.close()
    except:
        print("Admin table error")

# customer table creation


def customer():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue, database="atm")
        cur = db.cursor()
        cur.execute('''create table if not exists customer(
            customer_id varchar(50) primary key,
            first_name varchar(50),
            last_name varchar(50),
            last_login timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
            password varchar(20))''')
        accountDetails()
        cur.close()
        db.close()
    except:
        print("Customer table error")

# account details table creation


def accountDetails():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue, database="atm")
        cur = db.cursor()
        cur.execute('''create table if not exists account_details(
            account_no BigInt primary key,
            customer_id varchar(50) ,
            balance decimal,
            foreign key(customer_id) references customer(customer_id))''')
        db.commit()
        print("Tables created sucessfully")
        cur.close()
        db.close()
    except:
        print("Account details table error")


def createAdmin():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue, database="atm")
        cur = db.cursor()
        print("*****CREATE ADMIN*****")
        name = input("Enter UserName: ")
        password = input("Enter Password: ")
        confirm = input(("Do you want to confirm(y/n): "))
        if confirm == "y":
            query = "insert into admindb (username, password) values ('{}','{}')".format(
                name, password)
            cur.execute(query)
            db.commit()
            print("Admin Created Sucessfully!!")
        cur.close()
        db.close()
    except Exception as e:
        print("Admin Creation Error", e)


def addPredefinedCustomer():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue, database="atm")
        cur = db.cursor()
        customer = [["125452463", "Aman", "Das", "P@$$w0rd"],
                    ["125452464", "Sam", "Jerld", "P@$$w0rd"],
                    ["125452465", "Jian", "Goda", "P@$$w0rd"],
                    ["125452466", "Sunio", "Honikawa", "P@$$w0rd"],
                    ["125452467", "Daisy", "Willson", "P@$$w0rd"],
                    ["125452468", "shambhoo", "Kumar", "P@$$w0rd"],
                    ["125452469", "Priyanka", "Mehta", "P@$$w0rd"],
                    ["125452461", "Chinmoy", "Dutta", "P@$$w0rd"]]
        for [i, j, k, l] in customer:
            query = "insert into customer(customer_id, first_name, last_name, password) values('{}','{}','{}','{}')".format(
                i, j, k, l)
            cur.execute(query)
            db.commit()
        print("Customer Added Successfully")
        cur.close()
        db.close()
    except Exception as e:
        print("Add customer Error", e)


def addAccountDetails():
    try:
        db = mysql.connector.connect(
            host=hostValue, user=userValue, passwd=passwdValue, database="atm")
        cur = db.cursor()
        account_details = [[512125452463, "125452463", 100000],
                           [512125452464, "125452464", 150000],
                           [512125452465, "125452465", 160000],
                           [512125452466, "125452466", 150000],
                           [512125452467, "125452467", 180000],
                           [512125452468, "125452468", 170000],
                           [512125452469, "125452469", 230000],
                           [512125452461, "125452461", 590000]]
        for [i, j, k] in account_details:
            query = "insert into account_details(account_no, customer_id, balance) values('{}','{}','{}')".format(
                i, j, k)
            cur.execute(query)
            db.commit()
        print("Account_details Added Successfully")
        cur.close()
        db.close()
    except Exception as e:
        print("Add account_details Error", e)


def menu():
    print("-----------------------------------------------------------------------")
    print("***************************ATM MANAGEMENT***************************")
    return display()


def display():
    print("----------------------------------Main Menu-------------------------------------")
    choice = int(
        input(" \n1.Admin login\n2.Customer Menu\n3.Exit\nEnter choice: "))
    if choice == 1:
        try:
            admin_login()
        except:
            print("Admin login Error")
            display()

    elif choice == 2:
        try:
            customer_login()
            customer_menu()
        except:
            print("Customer_menu Error")
            display()

    elif choice == 3:
        print("THANK YOU FOR USING OUR ATM SYSTEM!!!")
        return
    else:
        display()


def customer_menu():
    print("--------------------------------Customer Menu---------------------------------------")
    choice = int(
        input(" \n1.Add Balance\n2.Withraw amount\n3.Exit\nEnter choice: "))
    if choice == 1:
        try:
            add_balance()
            customer_menu()
        except:
            print("Add balance Error")
            display()

    elif choice == 2:
        try:
            withdraw_balance()
            customer_menu()
        except:
            print("Withdraw balance Error")
            display()

    elif choice == 3:
        return display()


def add_balance():
    try:
        customer_id = input("Enter Customer Id: ")
        account_no = input("Enter Account Number: ")
        confirm = input(("Do you want to confirm(y/n): "))
        if confirm == "y":
            query = "select ad.balance from customer c join account_details ad on c.customer_id=ad.customer_id where ad.customer_id ='{}' and ad.account_no ={}".format(
                customer_id, account_no)
            cur.execute(query)
            result = cur.fetchall()
            if not result:
                print("Customer has no account or customer id is not valid one")
                return
            else:
                balance = result[0][0]
                print("Your available balance is: {}".format(str(balance)))
                dipositAmount = int(input("Enter amount you want to add: "))
                total_amount = balance + dipositAmount
                print("Your available balance after deposit is: {}".format(
                    str(total_amount)))
                query = "update account_details set balance = {} where customer_id ='{}' and account_no = {}".format(
                    total_amount, customer_id, account_no)
                cur.execute(query)
                db.commit()
        else:
            return customer_menu()
    except Exception as e:
        print("Add amount Error", e)


def withdraw_balance():
    try:
        customer_id = input("Enter Customer Id: ")
        account_no = input("Enter Account Number: ")
        confirm = input(("Do you want to confirm(y/n): "))
        if confirm == "y":
            query = "select ad.balance from customer c join account_details ad on c.customer_id=ad.customer_id where ad.customer_id ='{}' and ad.account_no ={}".format(
                customer_id, account_no)
            cur.execute(query)
            result = cur.fetchall()
            if not result:
                print("Customer has no account or customer id is not valid one")
                return
            else:
                balance = result[0][0]
                print("Your available balance is: {}".format(str(balance)))
                withdrawAmount = int(input("Enter amount you want to add: "))
                if(balance < withdrawAmount):
                    print("Sorry you dont have sufficient balance!!")
                    return customer_menu()
                else:
                    total_amount = balance - withdrawAmount
                    print("Your available balance after withdrawal is: {}".format(
                        str(total_amount)))
                    query = "update account_details set balance = {} where customer_id ='{}' and account_no = {}".format(
                        total_amount, customer_id, account_no)
                    cur.execute(query)
                    db.commit()
        else:
            return customer_menu()
    except Exception as e:
        print("Withdraw amount Error", e)


def registerCustomer():
    try:
        customer_id = input("Enter Customer Id: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        password = input("Enter Password: ")
        confirm = input(("Do you want to confirm(y/n): "))
        if confirm == "y":
            query = "insert into customer (customer_id, first_name, last_name, password) values ('{}','{}','{}','{}')".format(
                customer_id, first_name, last_name, password)
            cur.execute(query)
            db.commit()
            print("Customer Registered Sucessfully!!")
            return
        else:
            return registerCustomer()
    except Exception as e:
        print("Customer Registration Error", e)


def admin_login():
    try:
        username = input("Enter username: ")
        password = input("Enter Password: ")
        confirm = input(("Do you want to confirm(y/n): "))
        if confirm == "y":
            query = "select username from admindb where username='{}' AND password='{}'".format(
                username, password)
            cur.execute(query)
            records = cur.fetchall()
            if not records:
                print("Invalid Credentials")
                return admin_login()
            else:
                return admin_menu()
        else:
            return display()
    except Exception as e:
        print("Admin Login Error", e)


def customer_login():
    try:
        username = input("Enter username: ")
        password = input("Enter Password: ")
        confirm = input(("Do you want to confirm(y/n): "))
        if confirm == "y":
            query = "select customer_id from customer where customer_id='{}' AND password='{}'".format(
                username, password)
            cur.execute(query)
            records = cur.fetchall()
            if not records:
                print("Invalid Credentials")
                return customer_login()
            else:
                return customer_menu()
        else:
            return display()
    except Exception as e:
        print("Admin Login Error", e)


def admin_menu():
    print("-----------------------------Admin Menu------------------------------------------")
    choice = int(input(
        " \n1.Add New Customer\n2.Delete Existing Customer\n3.View Customer\n4.View Logs\n5.Exit\nEnter choice: "))
    if choice == 1:
        try:
            registerCustomer()
            admin_menu()
        except:
            print("Registration Error")
            display()

    elif choice == 2:
        try:
            delete_customer()
            admin_menu()
        except:
            print("Delete Customer Error")
            display()

    elif choice == 3:
        try:
            view_customer()
            admin_menu()
        except:
            print("Logs Error")
            display()

    elif choice == 4:
        try:
            get_logs()
            admin_menu()
        except:
            print("Logs Error")
            display()
    else:
        return display()


def view_customer():
    try:
        query = "select * from customer"
        cur.execute(query)
        res = cur.fetchall()
        if not res:
            print("Customer table is empty")
            admin_menu()
        else:
            for i, j, k, l, m in res:
                print("Customer Id: {}, First Name: {}, Last Name: {}, Last Login: {}, Password: {}".format(
                    str(i), str(j), str(k), str(l), str(m)))
            print("------------------------------------------")
            admin_menu()

    except Exception as e:
        print("Delete Customer Error as account exists", e)
        admin_menu()


def delete_customer():
    try:
        uid = int(input("Enter Customer ID: "))
        query = "select * from customer where customer_id=('{}')".format(uid)
        cur.execute(query)
        if not cur.fetchall():
            print("Customer with this ID doesn't exist")
            admin_menu()
        else:
            query = "delete from customer where customer_id=('{}')".format(uid)
            cur.execute(query)
            db.commit()
            print("Customer Deleted Successfully")
            admin_menu()

    except Exception as e:
        print("Delete Customer Error as account exists", e)
        admin_menu()


def log():
    myFile = open('Log_atm.txt', 'a')
    x = (datetime.now())
    z = ('\nAccessed by admin on '+str(x))
    myFile.write(z)
    myFile.close()


def get_logs():
    f = open("Log_atm.txt", "r")
    print(f.read())
    f.close()
    return


try:
    if os.path.exists("Log_atm.txt") == False:
        database()
        log()
        admin()
        createAdmin()
        addPredefinedCustomer()
        addAccountDetails()
    db = mysql.connector.connect(
        host=hostValue, user=userValue, passwd=passwdValue, database="atm")
    cur = db.cursor()
    menu()
    cur.close()
    db.close()
except Exception as e:
    print("Main Menu Error", e)
