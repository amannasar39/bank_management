
import mysql.connector

class Bank_db:

    def __init__(self):
        try:
            self.con = mysql.connector.connect(user="root",password="horsepower12@",host="localhost",database="bank_management")
            print(self.con)
        except:
            print("Connection failed")

    # Create Account
    def create(self,name,acc_type,phone,balance):
        try:
            if balance < 0:
                print("Balance cannot be negative")
                return

            cursor = self.con.cursor()
            query = "insert into accounts(customer_name,account_type,phone,balance) values(%s,%s,%s,%s)"
            data = (name,acc_type,phone,balance)
            cursor.execute(query,data)
            self.con.commit()
            print("Account created successfully")

        except:
            print("Failed to create account")

    # View Accounts
    def read(self):
        try:
            cursor = self.con.cursor()
            query = "select * from accounts order by balance desc"
            cursor.execute(query)
            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")

        except:
            print("Failed to read")

    # Filter Accounts
    def filter(self,amount):
        try:
            if amount < 0:
                print("Invalid amount")
                return

            cursor = self.con.cursor()
            query = "select * from accounts where balance >= %s order by balance desc"
            data = (amount,)
            cursor.execute(query,data)
            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")

        except:
            print("Failed to filter")

    # Search by Account ID
    def retrieve(self,id):
        try:
            cursor = self.con.cursor()
            query = "select * from accounts where account_id=%s"
            data = (id,)
            cursor.execute(query,data)
            record = cursor.fetchone()

            if record:
                print(record)
            else:
                print("No Records Found")

        except:
            print("Failed to retrieve")

    # Search by Customer Name
    def search(self,name):
        try:
            cursor = self.con.cursor()
            query = "select * from accounts where customer_name like %s"
            data = ("%" + name + "%",)
            cursor.execute(query,data)
            records = cursor.fetchall()

            if records:
                for row in records:
                    print(row)
            else:
                print("No Records Found")

        except:
            print("Failed to search")

    # Deposit
    def deposit(self,id,amount):
        try:
            if amount <= 0:
                print("Invalid amount")
                return

            cursor = self.con.cursor()
            query = "update accounts set balance=balance+%s where account_id=%s"
            data = (amount,id)
            cursor.execute(query,data)
            self.con.commit()

            if cursor.rowcount > 0:
                print("Amount deposited successfully")
            else:
                print("No record found")

        except:
            print("Failed to deposit")

    # Withdraw
    def withdraw(self,id,amount):
        try:
            if amount <= 0:
                print("Invalid amount")
                return

            cursor = self.con.cursor()
            query = "update accounts set balance=balance-%s where account_id=%s and balance >= %s"
            data = (amount,id,amount)
            cursor.execute(query,data)
            self.con.commit()

            if cursor.rowcount > 0:
                print("Withdrawal successful")
            else:
                print("Account not found or insufficient balance")

        except:
            print("Failed to withdraw")

    # Delete Account
    def delete(self,id):
        try:
            cursor = self.con.cursor()
            query = "select * from accounts where account_id=%s"
            data = (id,)
            cursor.execute(query,data)
            record = cursor.fetchone()

            if record:
                ch = input("Are you sure to delete? (y/n): ")

                if ch.lower() == "y":
                    query = "delete from accounts where account_id=%s"
                    cursor.execute(query,data)
                    self.con.commit()
                    print("Account deleted successfully")
                else:
                    print("Deletion cancelled")
            else:
                print("No record found")

        except:
            print("Failed to delete")


# Object Creation
b = Bank_db()

while(1):
    print("\nBank Management System")
    print("1.Create Account")
    print("2.View Accounts")
    print("3.Filter Accounts")
    print("4.Search Account by ID")
    print("5.Search Account by Name")
    print("6.Deposit Amount")
    print("7.Withdraw Amount")
    print("8.Delete Account")
    print("9.Exit")

    try:
        ch = int(input("Enter your choice:"))

        if ch == 1:
            n = input("Enter customer name:")
            t = input("Enter account type:")
            p = input("Enter phone number:")
            a = float(input("Enter opening balance:"))
            b.create(n,t,p,a)

        elif ch == 2:
            b.read()

        elif ch == 3:
            a = float(input("Enter minimum balance:"))
            b.filter(a)

        elif ch == 4:
            i = int(input("Enter account ID:"))
            b.retrieve(i)

        elif ch == 5:
            n = input("Enter customer name:")
            b.search(n)

        elif ch == 6:
            i = int(input("Enter account ID:"))
            a = float(input("Enter deposit amount:"))
            b.deposit(i,a)

        elif ch == 7:
            i = int(input("Enter account ID:"))
            a = float(input("Enter withdrawal amount:"))
            b.withdraw(i,a)

        elif ch == 8:
            i = int(input("Enter account ID:"))
            b.delete(i)

        elif ch == 9:
            print("Thank you")
            b.con.close()
            exit()

        else:
            print("Invalid Input")

    except ValueError:
        print("Enter valid input")
