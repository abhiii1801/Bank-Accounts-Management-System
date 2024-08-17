import sys
import random
import string
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6 import QtWidgets
from bank_sphere import Ui_BankSphere 
from db_manage import USER_Manage, ACCOUNTS_Manage, TRANSACTIONS_Manage
from receipt import Receipts
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        print("Class Created")
        super().__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.Window | QtCore.Qt.WindowType.WindowMinimizeButtonHint | QtCore.Qt.WindowType.WindowCloseButtonHint)

        self.ui = Ui_BankSphere()
        self.user_db = USER_Manage()
        self.ac_db = ACCOUNTS_Manage()
        self.tr_db = TRANSACTIONS_Manage()
        self.pr_rec = Receipts()
        self.ui.setupUi(self)

        self.ui.username_entry.setText("abhinav_tom24")
        self.ui.password_entry.setText("qwerty123")

        self.cuurent_frame = self.ui.homepage

        self.ui.homepage.setVisible(True)
        self.ui.register_frame.setVisible(False)
        self.ui.loggedin_homepage.setVisible(False)
        self.ui.profile_info.setVisible(False)
        self.ui.transfer_frame.setVisible(False)
        self.ui.tr_confirm_frame.setVisible(False)
        self.ui.tr_recipt_frame.setVisible(False)
        self.ui.ai_frame.setVisible(False)
        self.ui.ai_create_frame.setVisible(False)
        self.ui.ai_cbal_frame.setVisible(False)
        self.ui.admin_login_frame.setVisible(False)
        self.ui.add_mon_frame.setVisible(False)
        self.ui.transaction_frame.setVisible(False)

        self.ui.login_btn.clicked.connect(self.login_pressed)
        self.ui.register_btn.clicked.connect(self.register_pressed)

    def logged_init(self, username):
        print("LoggedIn()")
        self.cuurent_frame.setVisible(False)
        self.ui.loggedin_homepage.setVisible(True)

        self.ui.profile_btn.clicked.connect(lambda: self.profile_info(username))
        self.ui.acc_info_btn.clicked.connect(lambda: self.acc_info(username))
        self.ui.transfer_btn.clicked.connect(lambda: self.transfer_pressed(username))
        self.ui.transactionsbtn.clicked.connect(lambda: self.transactions_info(username))
        self.ui.add_mon_btn.clicked.connect(lambda: self.add_money())

    def login_pressed(self):
        print("Login Pressed()")
        username = self.ui.username_entry.text()
        password = self.ui.password_entry.text()

        if username and password:
            v = self.user_db.validate_user(username=username, pwd=password)
            if v == 0:
                QMessageBox.critical(self, "UserName Error", "Username Not Found !!")
            elif v == -1:
                QMessageBox.critical(self, "Password Error", "Incorrect Password !!")
            else:
                self.logged_init(username)
        else:
            QMessageBox.critical(self, "Error", "Please Fill in the Required Fields")

    def register_pressed(self):
        print("Register Pressed()")
        
        def generate_user_name():
            print("Generated User Name")
            first_name = self.ui.firstname_entry.text()
            last_name = self.ui.lastname_entry.text()
            if first_name and last_name:
                rand_name = f"{first_name.lower()}_{last_name.lower()[:3]}{random.randint(10, 99)}"
                self.ui.username_register_entry.setText(rand_name)
            else:
                QMessageBox.critical(self, "Error", "First Name and Last Name must be filled to generate a username")
        
        def back_to_login():
            print("Back to Login")
            self.ui.register_frame.setVisible(False)
            self.ui.homepage.setVisible(True)

        def register_btn_pressed():
            print("Register Button Pressed")
            user_data = {
                "first_name": self.ui.firstname_entry.text(),
                "last_name": self.ui.lastname_entry.text(),
                "dob": self.ui.date_entry.text(),
                "username": self.ui.username_register_entry.text(),
                "password": self.ui.password_register_entry.text(),
                "email": "",
                "phone": "",
                "address": ""
            }
            if self.ui.firstname_entry.text() and self.ui.lastname_entry.text() and self.ui.date_entry.text() and self.ui.username_register_entry.text() and self.ui.password_register_entry.text():
                v = self.user_db.add_user(user_data=user_data)
                if v == 0:
                    QMessageBox.critical(self, "UserName Error", "Username already exists !!")
                else:
                    info = QMessageBox()
                    info.setIcon(QMessageBox.Icon.Information)
                    info.setText("Account successfully created")
                    info.setWindowTitle("Success!!")
                    info.setStandardButtons(QMessageBox.StandardButton.Ok)
                    info.buttonClicked.connect(back_to_login)
                    info.exec()
            else:
                QMessageBox.critical(self, "Error", "Please Fill in the Required Fields")

        self.ui.homepage.setVisible(False)
        self.ui.register_frame.setVisible(True)
        self.ui.register_form_btn.clicked.connect(register_btn_pressed)
        self.ui.generate_username_btn.clicked.connect(generate_user_name)

    def profile_info(self, username):
        print("Profile Info")
        self.cuurent_frame.setVisible(False)
        self.cuurent_frame = self.ui.profile_info

        user_info = self.user_db.retrive_user_info(username)
        
        self.ui.p_firstname.setText(user_info["first_name"])
        self.ui.p_lastname.setText(user_info["last_name"])
        self.ui.p_username.setText(username) 
        self.ui.p_phonenum.setText(user_info['phone']) if user_info['phone'] != '' else self.ui.p_phonenum.setText("-")
        self.ui.p_dob.setText(user_info['dob'])
        self.ui.p_email.setText(user_info['email']) if user_info["email"] != '' else self.ui.p_email.setText("-")
        self.ui.p_address.setText(user_info['address']) if user_info['address'] != '' else self.ui.p_address.setText("-")

        def toggle_edit_mode(editing):
            if editing:
                self.ui.p_address.hide()
                self.ui.p_phonenum.hide()
                self.ui.p_email.hide()
                
                self.ui.p_address_input = QtWidgets.QLineEdit(parent=self.ui.profile_info)
                self.ui.p_address_input.setGeometry(QtCore.QRect(470, 450, 331, 31))
                self.ui.p_address_input.setFont(self.ui.p_address.font())
                # self.ui.p_address_input.setText(user_info['address'])
                self.ui.p_address_input.show()
                
                self.ui.p_phonenum_input = QtWidgets.QLineEdit(parent=self.ui.profile_info)
                self.ui.p_phonenum_input.setGeometry(QtCore.QRect(470, 500, 331, 31))
                self.ui.p_phonenum_input.setFont(self.ui.p_phonenum.font())
                # self.ui.p_phonenum_input.setText(user_info['phone'])
                self.ui.p_phonenum_input.show()

                self.ui.p_email_input = QtWidgets.QLineEdit(parent=self.ui.profile_info)
                self.ui.p_email_input.setGeometry(QtCore.QRect(470, 550, 331, 31))
                self.ui.p_email_input.setFont(self.ui.p_email.font())
                # self.ui.p_email_input.setText(user_info['email'])
                self.ui.p_email_input.show()

                self.ui.p_edit_profile_btn.setText("Save")
                self.ui.p_edit_profile_btn.clicked.disconnect()
                self.ui.p_edit_profile_btn.clicked.connect(lambda: toggle_edit_mode(False))
            else:
                new_address = self.ui.p_address_input.text()
                new_phone = self.ui.p_phonenum_input.text()
                new_email = self.ui.p_email_input.text()

                self.user_db.update_user_info(username, new_address, new_phone, new_email)
                
                self.ui.p_address.setText(new_address)
                self.ui.p_phonenum.setText(new_phone)
                self.ui.p_email.setText(new_email)

                self.ui.p_address_input.hide()
                self.ui.p_phonenum_input.hide()
                self.ui.p_email_input.hide()

                self.ui.p_address.show()
                self.ui.p_phonenum.show()
                self.ui.p_email.show()

                self.ui.p_edit_profile_btn.setText("Edit")
                self.ui.p_edit_profile_btn.clicked.disconnect()
                self.ui.p_edit_profile_btn.clicked.connect(lambda: toggle_edit_mode(True))

        self.ui.p_edit_profile_btn.clicked.connect(lambda: toggle_edit_mode(True))
        self.ui.profile_info.setVisible(True)

    def acc_info(self, username):
        print("Account Info Main")
        self.cuurent_frame.setVisible(False)
        self.cuurent_frame = self.ui.ai_frame
        banks = ['AXIS', 'SBI', 'HDFC', 'ICICI', 'KOTAK', 'PNB', 'IDFC']

        def add_acc():
            print("Add Account Pressed")
            def acc_create_pressed():
                print("Account Create Pressed")
                pin = str(self.ui.ai_cr_pin.text())
                if len(pin) == 4:
                    bank = self.ui.ai_cr_bank.currentText()
                    account_type = self.ui.ai_cr_type.currentText()
                    if pin and bank and account_type:
                        account_data = {
                            "username": username,
                            "bank": bank,
                            "account_type": account_type,
                            "balance": 0,
                            "pin": pin
                        }
                        v = self.ac_db.create_account(account_data=account_data)
                        if v == 0:
                            QMessageBox.critical(self, "Error", "Account Creation Failed")
                        else:
                            QMessageBox.information(self, "Success", "Account Created Successfully")
                            self.ui.acc_info_btn.click()
                else:
                    QMessageBox.critical(self, "Error", "Please Enter 4 digit PIN")

            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.ai_create_frame
            self.ui.ai_cr_bank.clear()
            self.ui.ai_cr_bank.addItems(banks)
            acc_types = ['Savings', 'Current']
            self.ui.ai_cr_type.clear()
            self.ui.ai_cr_type.addItems(acc_types)
            self.ui.ai_cr_pin.clear()

            self.ui.ai_create_frame.setVisible(True)
            try:
                self.ui.ai_cr_btn.clicked.disconnect()
            except:
                pass
            self.ui.ai_cr_btn.clicked.connect(acc_create_pressed)
        
        def check_bal():
            print("Check Balance Pressed")
            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.ai_cbal_frame

            self.ui.ai_cbal_cb.setVisible(False)
            self.ui.ai_cbal_bal.setVisible(False)
            
            def check_bal_pressed():
                print("Retrive Balance Pressed")
                bank = self.ui.ai_cbal_bank.currentText()
                acc_num = self.ui.ai_cbal_accnum.currentText()
                acc_pin = self.ui.ai_cbal_pin.text()

                if bank and acc_num and acc_pin:
                    ma = self.ac_db.check_acc_num_with_bank(acc_num, bank)
                    if ma == 1:
                        cp = self.ac_db.validate_pin(int(acc_pin), acc_num)
                        if cp == 1:
                            bal = self.ac_db.retrive_balance(acc_num)
                            if bal:
                                self.ui.ai_cbal_bal.setText(str(bal))
                                self.ui.ai_cbal_cb.setVisible(True)
                                self.ui.ai_cbal_bal.setVisible(True)
                            else:
                                QMessageBox.critical(self, "Error", "Account Not Found!!")
                        else:
                            QMessageBox.critical(self, "Error", "Incorrect PIN!!")
                    else:
                        QMessageBox.critical(self, "Error", "Bank and Account Number Mismatch!!")
                else:
                    QMessageBox.critical(self, "Error", "Please Fill in the Required Fields")
            
            def setaccounts(accounts):
                print("Set Accounts Pressed")
                bank_selected = self.ui.ai_cbal_bank.currentText()
                accounts_ids = [str(account[0]) for account in accounts if account[1] == bank_selected]
                self.ui.ai_cbal_accnum.clear()
                self.ui.ai_cbal_accnum.addItems(accounts_ids)

            accounts = self.ac_db.retrive_all_accounts(username)
            banks_unique = list({bank[1] for bank in accounts})

            self.ui.ai_cbal_bank.clear()
            self.ui.ai_cbal_bank.addItems(banks_unique)

            self.ui.ai_cbal_accnum.clear()
            self.ui.ai_cbal_pin.clear()

            try:
                self.ui.ai_cbal_btn.clicked.disconnect()
                self.ui.ai_cbal_list_acc.clicked.disconnect()
            except:
                pass
            self.ui.ai_cbal_list_acc.clicked.connect(lambda: setaccounts(accounts))
            self.ui.ai_cbal_btn.clicked.connect(check_bal_pressed)

            self.ui.ai_cbal_frame.setVisible(True)

        data = self.ac_db.retrive_account_info(username)
        if data is not None:
            self.ui.ai_check_bal_btn.setVisible(True)
            self.ui.ai_table.setVisible(True)
            self.ui.ai_acc_labels.setText(f'{len(data)} Accounts Found')
            self.ui.ai_table.setRowCount(len(data))
            for row_idx, row_data in enumerate(data):
                for col_idx, item in enumerate(row_data):
                    self.ui.ai_table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        else:
            self.ui.ai_check_bal_btn.setVisible(False)
            self.ui.ai_table.setVisible(False)

        try:
            self.ui.ai_add_acc_btn.clicked.disconnect()
            self.ui.ai_check_bal_btn.clicked.disconnect()
        except:
            pass

        self.ui.ai_add_acc_btn.clicked.connect(add_acc)
        self.ui.ai_check_bal_btn.clicked.connect(check_bal)
        self.ui.ai_frame.setVisible(True)

    def transfer_pressed(self, username):
        print("Main Transfer Pressed")
        self.cuurent_frame.setVisible(False)
        self.cuurent_frame = self.ui.transfer_frame
        self.ui.tr_reciever_acc.clear()
        self.ui.tr_amt.clear()
        self.ui.trc_pin_entry.clear()

        try:
            self.ui.tr_list_acc.clicked.disconnect()
        except:
            pass 

        try:
            self.ui.tr_cont.clicked.disconnect()
        except:
            pass 

        def set_accounts(accounts):
            print("Set Accounts")
            bank = self.ui.tr_bank.currentText()
            accounts_ids = [str(account[0]) for account in accounts if account[1] == bank]
            self.ui.tr_sender_acc.clear()
            self.ui.tr_sender_acc.addItems(accounts_ids)

        def transfer_cont_pressed():
            print("Transfer Cont Pressed")
            if self.ui.tr_sender_acc.currentText() and self.ui.tr_reciever_acc.text() and self.ui.tr_amt.text():
                ma = self.ac_db.check_acc_num_with_bank(self.ui.tr_sender_acc.currentText(), self.ui.tr_bank.currentText())
                if ma == 1:
                    tr = self.ac_db.validate_acc_num(self.ui.tr_reciever_acc.text())
                    if tr == 1:
                        v = self.ac_db.validate_balance(self.ui.tr_sender_acc.currentText(), int(self.ui.tr_amt.text()))
                        if v == 1:
                            transfer_confirm()
                        elif v == 0:
                            QMessageBox.critical(self, "Error", "Insufficient Balance")
                        else:
                            QMessageBox.critical(self, "Error", "Error")
                    elif tr == 0:
                        QMessageBox.critical(self, "Error", "Invalid RECIEVER Account Number")
                    else:
                        QMessageBox.critical(self, "Error", "Error")
                else:
                    QMessageBox.critical(self, "Error", "Bank and Account Number Mismatch !!")
            else:
                QMessageBox.critical(self, "Error", "Please Fill in the Required Fields")

        def cancel_transaction():
            print("Cancel Transaction")
            self.cuurent_frame.setVisible(False)
            self.ui.transfer_frame.setVisible(True)
            self.cuurent_frame = self.ui.transfer_frame

        def back_to_home():
            print("Back to Home")
            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.homepage
            self.ui.homepage.setVisible(True)

        def transaction_success():
            print("Transaction Success")
            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.tr_recipt_frame

            random_letters = ''.join(random.choices(string.ascii_lowercase, k=5))
            random_numbers = ''.join(random.choices(string.digits, k=5))
            tr_id = random_letters + random_numbers

            t = self.ac_db.tranfer_funds(self.ui.tr_sender_acc.currentText(), self.ui.tr_reciever_acc.text(), self.ui.tr_amt.text(), tr_id)

            if t == 1:
                self.ui.tr_recipt_frame.setVisible(True)
                self.ui.tr_rec_trans_id.setText(tr_id)
                try:
                    self.ui.tr_rec_print.clicked.disconnect()
                    self.ui.tr_rec_home.clicked.disconnect()
                except:
                    pass

                self.ui.tr_rec_print.clicked.connect(lambda: print_receipt(tr_id))
                self.ui.tr_rec_home.clicked.connect(back_to_home)
            else:
                QMessageBox.critical(self, "Error", "Error")

        def pin_entered():
            print("Pin Verification")
            pin = self.ui.trc_pin_entry.text()
            if len(pin) != 4:
                QMessageBox.critical(self, "Error", "Please Enter a Valid Pin")
            elif not pin.isdigit():
                QMessageBox.critical(self, "Error", "Please Enter a Valid Pin")
            else:
                pin_verify = self.ac_db.validate_pin(int(pin), self.ui.tr_sender_acc.currentText())
                if pin_verify == 1:
                    transaction_success()
                else:
                    QMessageBox.critical(self, "Error", "Invalid PIN")

        def transfer_confirm():
            print("Transfer Confirm")
            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.tr_confirm_frame

            self.ui.trc_amt.setText(self.ui.tr_amt.text())

            self.sen_name = self.ac_db.retrive_name(self.ui.tr_sender_acc.currentText())
            self.rec_name = self.ac_db.retrive_name(self.ui.tr_reciever_acc.text())

            self.ui.trc_sender_name.setText(self.sen_name)
            self.ui.trc_sender_acc.setText(self.ui.tr_sender_acc.currentText())

            self.ui.trc_reciever_name.setText(self.rec_name)
            self.ui.trc_reciever_acc.setText(self.ui.tr_reciever_acc.text())

            # Disconnect old connections before connecting new ones
            try:
                self.ui.trc_verify.clicked.disconnect()
                self.ui.trc_cancel.clicked.disconnect()
            except:
                pass
            
            self.ui.trc_verify.clicked.connect(pin_entered)
            self.ui.trc_cancel.clicked.connect(cancel_transaction)
            self.ui.tr_confirm_frame.setVisible(True)

        def print_receipt(tr_id):
            print("Print Receipt")

            rec_bank = self.ac_db.retrive_bank_name(self.ui.tr_sender_acc.currentText())

            v = self.pr_rec.create_transaction_receipt(
                sender_name=self.sen_name,
                sender_accnum=self.ui.tr_sender_acc.currentText(),
                sender_acc_type="Savings",
                sender_bank=self.ui.tr_bank.currentText(),
                receiver_name=self.rec_name,
                receiver_accnum=self.ui.trc_reciever_acc.text(),
                receiver_bank=rec_bank,
                transaction_amount=f"₹{self.ui.tr_amt.text()}",
                transaction_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                transaction_id=tr_id
            )

            if v == 1:
                QMessageBox.information(self, "Success", "Printed Successfully")
                back_to_home()
            # print("Reciept Printed\nTransaction ID: ", tr_id)


        accounts = self.ac_db.retrive_all_accounts(username)
        banks = list({bank[1] for bank in accounts})
        self.ui.tr_bank.clear()
        self.ui.tr_bank.addItems(banks)
        self.ui.transfer_frame.setVisible(True)

        self.ui.tr_list_acc.clicked.connect(lambda: set_accounts(accounts))
        self.ui.tr_cont.clicked.connect(transfer_cont_pressed)

    def transactions_info(self, username):
        
        def back_to_home():
            print("Back to Home")
            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.homepage
            self.ui.homepage.setVisible(True)

        print("Transactions Info Main")
        self.cuurent_frame.setVisible(False)
        self.cuurent_frame = self.ui.transaction_frame

        accounts = self.ac_db.retrive_all_accounts(username)
        banks_unique = list({bank[1] for bank in accounts})
        accounts_ids = [str(account[0]) for account in accounts ]
        re = self.tr_db.retrive_all_transactions(username)

        def retrive_all_trans():
            print("All Accounts")
            self.ui.trans_option_box.setVisible(False)
            self.ui.trans_retrive_tbn.setVisible(False)
            self.ui.trans_table.clearContents()
            if re:
                self.ui.trans_table.setRowCount(len(re))
                for i, row in enumerate(re):
                    for j, col in enumerate(row):
                        self.ui.trans_table.setItem(i, j, QTableWidgetItem(str(col)))

        def retrive_bank_trans():
            def bank_trans_clicked():
                bank_selected  = self.ui.trans_option_box.currentText()
                re = self.tr_db.retrive_bank_transactions(username, bank_selected)
                if re:
                    self.ui.trans_table.setRowCount(len(re))
                    for i, row in enumerate(re):
                        for j, col in enumerate(row):
                            self.ui.trans_table.setItem(i, j, QTableWidgetItem(str(col)))
                


            print("Bank Transaction")
            self.ui.trans_option_box.setVisible(True)
            self.ui.trans_retrive_tbn.setVisible(True)

            self.ui.trans_option_box.clear()
            self.ui.trans_option_box.addItems(banks_unique)

            try:
                self.ui.trans_retrive_tbn.clicked.disconnect()
            except:
                pass

            self.ui.trans_retrive_tbn.clicked.connect(bank_trans_clicked)

            self.ui.trans_table.clearContents()
            self.ui.trans_table.setRowCount(0)

        def retrive_acc_trans():
            def acc_trans_clicked():
                acc_selected  = self.ui.trans_option_box.currentText()
                re = self.tr_db.retrive_account_transactions(username, acc_selected)
                if re:
                    self.ui.trans_table.setRowCount(len(re))
                    for i, row in enumerate(re):
                        for j, col in enumerate(row):
                            self.ui.trans_table.setItem(i, j, QTableWidgetItem(str(col)))

            print("Account Transaction")
            self.ui.trans_option_box.setVisible(True)
            self.ui.trans_retrive_tbn.setVisible(True)

            self.ui.trans_option_box.clear()
            self.ui.trans_option_box.addItems(accounts_ids)

            try:
                self.ui.trans_retrive_tbn.clicked.disconnect()
            except:
                pass

            self.ui.trans_retrive_tbn.clicked.connect(acc_trans_clicked)

            self.ui.trans_table.clearContents()
            self.ui.trans_table.setRowCount(0)

        def print_passbook():
            print("Print Passbook")
            full_name = self.tr_db.retrive_info(username)
            print_pass = self.pr_rec.print_passbook(
                name=full_name,
                transactions=re
            )

            if print_pass == 1:
                QMessageBox.information(self, "Success", "Passbook Printed Successfully")
                back_to_home()


        try:
            self.ui.trans_accnum_opt.disconnect()
            self.ui.trans_bank_opt.disconnect()
            self.ui.trans_all_opt.disconnect()
            self.ui.print_trans_btn.disconnect()
        except:
            pass
        
        self.ui.trans_option_box.setVisible(False)
        self.ui.trans_retrive_tbn.setVisible(False)

        self.ui.trans_all_opt.toggled.connect(retrive_all_trans)
        self.ui.trans_bank_opt.toggled.connect(retrive_bank_trans)
        self.ui.trans_accnum_opt.toggled.connect(retrive_acc_trans)
        self.ui.print_trans_btn.clicked.connect(print_passbook)

        self.ui.transaction_frame.setVisible(True)

    def add_money(self):
        print("Add Money Main")
        self.cuurent_frame.setVisible(False)
        self.cuurent_frame = self.ui.admin_login_frame

        def admin_logged_in():
            print("Admin Logged In")
            self.cuurent_frame.setVisible(False)
            self.cuurent_frame = self.ui.add_mon_frame


            def admin_add_money():
                print("Admin Add Money")
                acc_num = self.ui.add_mon_accnum.currentText()
                try:
                    amount = int(self.ui.add_mon_amt.text())
                    if amount < 0:
                        raise
                    v = self.ac_db.admin_add_money(int(amount), acc_num)
                    if v == 1:
                        QMessageBox.information(self, "Success", "Money Added Successfully")
                        self.ui.add_mon_btn.click()
                    else:
                        QMessageBox.critical(self, "Error", "Error")

                except:
                    QMessageBox.critical(self, "Error", "Invalid Amount")
                
                self.ui.add_mon_accnum.clear()
                self.ui.add_mon_amt.clear()

            def set_accounts(accounts):
                print("Set Accounts Pressed")
                bank_selected = self.ui.add_mon_bank.currentText()
                accounts_ids = [str(account[0]) for account in accounts if account[1] == bank_selected]
                self.ui.add_mon_accnum.clear()
                self.ui.add_mon_accnum.addItems(accounts_ids)

            try:
                self.ui.add_mon_add_btn.clicked.disconnect()
                self.ui.add_mon_lis_acc.clicked.disconnect()
            except:
                pass
            
            accounts = self.ac_db.admin_all_accounts()
            banks_unique = list({bank[1] for bank in accounts})

            self.ui.add_mon_bank.clear()
            self.ui.add_mon_bank.addItems(banks_unique)

            self.ui.add_mon_lis_acc.clicked.connect(lambda: set_accounts(accounts))
            self.ui.add_mon_add_btn.clicked.connect(admin_add_money)

            self.ui.add_mon_frame.setVisible(True)

        def admin_login():
            print("Admin Login")
            username = self.ui.admin_user.text()
            password = self.ui.admin_password.text()

            if username and password:
                print(username, password)
                ad = self.user_db.validate_admin(username=username, pwd=password)
                if ad == 1:
                    admin_logged_in()
                else:
                    QMessageBox.critical(self, "Error", "Invalid Username or Password")
            else:
                QMessageBox.critical(self, "Error", "Please Enter Username and Password")

        try:
            self.ui.admin_login_btn.clicked.disconnect()
        except:
            pass
        
        self.ui.admin_user.clear()
        self.ui.admin_password.clear()
        self.ui.admin_login_btn.clicked.connect(admin_login)
        self.ui.admin_login_frame.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
