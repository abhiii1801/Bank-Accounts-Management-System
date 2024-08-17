import sqlite3
import datetime
import random

con = sqlite3.connect('banking_data.db')

def create_tables():
        try:
            con.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    password VARCHAR(50) NOT NULL,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100),
                    phone VARCHAR(15),
                    dob TEXT,
                    address TEXT
                );
            ''')
            con.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    bank VARCHAR(20),
                    account_type VARCHAR(20),
                    balance REAL,
                    created_date TEXT,
                    pin INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
            ''')
            con.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id VARCHAR(50) PRIMARY KEY,
                    sender_account_id INTEGER,
                    receiver_account_id INTEGER,
                    amount REAL,
                    transaction_date TEXT,
                    FOREIGN KEY (sender_account_id) REFERENCES accounts(account_id),
                    FOREIGN KEY (receiver_account_id) REFERENCES accounts(account_id)
                );
            ''')
            con.commit()
            return True
        except sqlite3.Error as e:
            print(e)
            return False

class USER_Manage: 
    def __init__(self) -> None:
        self.con = con

    def add_user(self,user_data):
        try:
            self.con.execute('''
                INSERT INTO users (username, password, first_name, last_name, email, phone, dob, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_data['username'], user_data["password"], user_data['first_name'], user_data['last_name'], user_data['email'], user_data['phone'], user_data['dob'], user_data['address']))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while adding a user: {e}")           

    def validate_user(self,username: str, pwd: str):
        try:
            cursor = self.con.execute('SELECT username, password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result:
                if result[1] == pwd:
                    return 1                                            # 1 : Both Username and Pwd correct
                else:
                    return -1                                           # -1 : Incorrect Password
            else:
                return 0                                                # 0 : User not found
        except sqlite3.Error as e:
            print(e)
    
    def retrive_user_info(self,username):
        cursor = self.con.execute('Select first_name, last_name, email, phone, dob, address from users where username = ?',(username,))
        result = cursor.fetchone()
        user_info = {
            "first_name": result[0],
            "last_name": result[1],
            "email": result[2],
            "phone":result[3],
            "dob":result[4],
            "address": result[5]
        }
        return user_info

    def validate_admin(self,username: str, pwd: str):
        try:
            cursor = self.con.execute('SELECT username, password FROM users WHERE role = "admin"')
            result = cursor.fetchone()
            if result:
                if result[1] == pwd and result[0] == username:
                    return 1                                            
                else:
                    return -1                                           
        except sqlite3.Error as e:
            print(e)
            return 0

    def update_user_info(self, username, new_address, new_phone, new_email):
        cursor = self.con.execute("UPDATE users SET address = ?, phone = ?, email = ? WHERE username = ?", (new_address, new_phone, new_email, username))

        self.con.commit()

class ACCOUNTS_Manage:
    def __init__(self) -> None:
        self.con = con

    def create_account(self,account_data):
        try:
            account_num = str(random.randint(100000000, 999999999))
            created_date = datetime.datetime.now().strftime("%d-%m-%Y")

            cursor = con.execute("SELECT user_id FROM users WHERE username = ?", (account_data['username'],))
            account_data['user_id'] = cursor.fetchone()[0]

            self.con.execute("INSERT INTO accounts VALUES(?,?,?,?,?,?,?)",(account_num,account_data['user_id'],account_data['bank'],account_data['account_type'],account_data['balance'],created_date, account_data['pin']))

            self.con.commit()

            return 1

        except sqlite3.Error as e:
            print(e)
            return 0
    
    def retrive_all_accounts(self,username):
        cursor = self.con.execute("Select accounts.account_id, accounts.bank, accounts.account_type, accounts.balance from accounts join users on accounts.user_id = users.user_id where users.username = ?",(username,))
        result = cursor.fetchall()
        return result

    def validate_acc_num(self, acc_num):
        try:
            cursor = self.con.execute(" Select account_id from accounts where account_id = ?",(acc_num,))
            result = cursor.fetchone()
            if result != None:
                return 1
            return 0
        except sqlite3.Error as e:
            print(e)
            return -1
    
    def validate_balance(self, acc_num,amount):
        try:
            cursor = self.con.execute("Select balance from accounts where account_id = ?",(acc_num,))

            result = cursor.fetchone()

            if result[0] >= amount:
                return 1
            else:
                return 0
            
        except sqlite3.Error as e:
            return -1
    
    def retrive_name(self,acc_num):
        cursor = self.con.execute("select users.first_name, users.last_name from users join accounts on users.user_id = accounts.user_id where accounts.account_id = ?;", (acc_num,));
        result = cursor.fetchone()
        full_name = " ".join(result)
        return full_name

    def validate_pin(self,pin,acc_num):
        cursor = self.con.execute("Select pin from accounts where account_id = ?",(acc_num,))
        result = cursor.fetchone()
        if result[0] == pin:
            return 1
        else:
            return 0

    def tranfer_funds(self, sender, reciever, amount, tr_id):
        try:
            self.con.execute("Update accounts set balance = balance - ? where account_id = ?;",(amount, sender))
            self.con.execute("Update accounts set balance = balance + ? where account_id = ?;",(amount, reciever))

            cuurent_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.con.execute("INSERT INTO transactions VALUES(?,?,?,?,?)",(tr_id,sender,reciever,amount,cuurent_time))

            self.con.commit()

            return 1
        except sqlite3.Error as e:
            print(e)
            return -1

    def retrive_bank_name(self,acc_num):
        cursor = self.con.execute("Select bank from accounts where account_id = ?",(acc_num,))
        result = cursor.fetchone()
        return result[0]
    
    def check_acc_num_with_bank(self,acc_num,bank):
        cursor = self.con.execute("Select account_id from accounts where account_id = ? and bank = ?",(acc_num,bank))
        result = cursor.fetchone()
        if result:
            return 1
        else:
            return 0

    def retrive_account_info(self,username):
        cursor = self.con.execute("Select accounts.bank, accounts.account_id, accounts.account_type, users.first_name || ' ' || users.last_name AS full_name ,accounts.created_date from accounts join users on accounts.user_id = users.user_id where users.username = ?",(username,))
        result = cursor.fetchall()
        if result:
            return result
        else:
            return None

    def retrive_balance(self,acc_num):
        cursor = self.con.execute("Select balance from accounts where account_id = ?",(acc_num,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0

    def admin_add_money(self,amount,acc_num):
        try:
            self.con.execute("Update accounts set balance = balance + ? where account_id = ?;",(amount, acc_num))
            self.con.commit()
            return 1
        except sqlite3.Error as e:
            print(e)
            return -1
        
    def admin_all_accounts(self):
        cursor = self.con.execute("Select account_id, bank from accounts")
        result = cursor.fetchall()
        return result

class TRANSACTIONS_Manage:
    def __init__(self):
        self.con = con  
    
    def retrive_all_transactions(self,username):
        cursor = self.con.execute("Select t.transaction_id, t.sender_account_id, t.receiver_account_id, t.amount, t.transaction_datetime from transactions as t join accounts as a on t.sender_account_id = a.account_id where a.user_id = (Select user_id from users where username = ?);",(username,))
        result = cursor.fetchall()
        return result
    
    def retrive_bank_transactions(self,username,bank):
        cursor = self.con.execute("Select t.transaction_id, t.sender_account_id, t.receiver_account_id, t.amount, t.transaction_datetime from transactions as t join accounts as a on t.sender_account_id = a.account_id where a.user_id = (Select user_id from users where username = ?) and a.bank = ?;", (username, bank))
        result = cursor.fetchall()
        return result
    
    def retrive_account_transactions(self,username ,acc_num):
        cursor = self.con.execute("Select t.transaction_id, t.sender_account_id, t.receiver_account_id, t.amount, t.transaction_datetime from transactions as t join accounts as a on t.sender_account_id = a.account_id where a.user_id = (Select user_id from users where username = ?) and a.account_id = ?;", (username, acc_num))
        result = cursor.fetchall()
        return result
    
    def retrive_info(self,username):
        cursor = self.con.execute("Select first_name, last_name from users where username = ?",(username,))
        result = cursor.fetchone()
        return " ".join(result)