import sys
import re
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def loadUserInfo():
    try:
        with open('userInfo.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def saveUserInfo():
    with open('userInfo.json', 'w') as file:
        json.dump(userInfo, file, indent=4)

def loadExpenses():
    try:
        with open('expensesData.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def saveExpenses():
    with open('expensesData.json', 'w') as file:
        json.dump(expenses, file, indent=4)

userInfo = loadUserInfo()
expenses = loadExpenses()

def isValidPassword(password):
    if len(password) < 6:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if re.search(r"[@#$%^&*()_+=\-{}\[\]:;\"'<>,.?/~]", password):
        return False
    return True

def main():
    print("\n------------------------------------------------------------")
    print("|                    WELCOME TO EXPENSIFY!                 |".center(60))
    print("------------------------------------------------------------")
    while True:
        entryInput = input("[Sign In] – [Sign Up] - [Exit] \nSelect here: ")
        if entryInput.lower() == "sign in":
            signIn()
        elif entryInput.lower() == "sign up":
            signUp()
        elif entryInput.lower() == "exit":
            exitProgram()
        else:
            print("\nInvalid Input. Please try again.\n")

def signIn():
    while True:
        emailInput = input("\nEmail: ")
        if emailInput in userInfo:
            forgotPassword = input("[1] - Proceed or [2] - Forgot Password? \nSelect here: ")
            if forgotPassword == "1":
                passwordInput = input("Password: ")
                if passwordInput == userInfo[emailInput]["password"]:
                    print(f"\nHello, {userInfo[emailInput]['username']}!")
                    showDashboard(emailInput)
                    return
                else:
                    print("\nIncorrect Password. Try Again.")
            elif forgotPassword == "2":
                sendPasswordViaEmail(emailInput)
                return
            else:
                print("\nInvalid Option. Please Select [1] or [2].")
        else:
            print("\nEmail Not Found. \nPlease Create An Account First.")
            while True:
                choice = input("\nBack to Main Menu? \n------------------ \n[Yes] or [No] \nSelect here:  ").lower()
                if choice in ["yes", "y"]:
                    return 
                elif choice in ["no", "n"]:
                    exitProgram()
                else:
                    print("\nInvalid Input. Please try again.")
            
def sendPasswordViaEmail(email):
    recipient = email
    senderEmail = email
    senderPassword = input("\nApp Password for Email: ")

    subject = "Password Recovery"
    body = f"Hello {userInfo[email]['username']},\n\nHere is your password for Expense Tracker: {userInfo[email]['password']}\n\nPlease keep this information secure.\n"

    message = MIMEMultipart()
    message['From'] = senderEmail
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(senderEmail, senderPassword)
            server.send_message(message)
            print("\nEmail Sent Successfully!\n")
    except Exception as e:
        print(f"Error Sending Email: {e}")
                
def signUp():
    emailInput = input("\nEnter your Email: ")
    if emailInput in userInfo:
        print("\nEmail Already Exists. Please Try Again.\n")
    else:
        usernameInput = input("Enter your Username: ")
        passwordInput = input("Enter your Password: ")
        confirmPassword = input("Confirm Password: ")
        if passwordInput != confirmPassword:
            print("\nPasswords Do Not match. Please Try Again.\n")
        elif not isValidPassword(passwordInput):
            print("\nPassword must contain at least 1 capital letter, 1 small letter, \n1 number, no special characters, and be at least 6 characters long.\n")
        else:
            userInfo[emailInput] = {"username": usernameInput, "password": passwordInput}
            saveUserInfo()
            print("\nAccount Created. You Can Now Sign In!\n")
            sendWelcomeEmail(emailInput, usernameInput)

def sendWelcomeEmail(email, username):
    recipient = email
    senderEmail = email
    senderPassword = input("App Password for Email: ")

    subject = "Welcome to EXPENSIFY! – Your Journey to Smarter Expense Tracking Begins Now!"
    body = f"""
    Hi {username},

    Welcome to EXPENSIFY!  
    We’re thrilled to have you on board and excited to help you track your expenses with ease and efficiency.

    With Expensify, managing your finances has never been simpler. You can now:

    - Keep track of all your expenses in one place.
    - Categorize and organize expenses effortlessly.
    - Stay on top of your budget with ease.

    We are committed to making your experience as smooth as possible, and we're here to support you every step of the way. 
    Feel free to reach out if you have any questions or feedback – we’d love to hear from you!

    Thanks for choosing EXPENSIFY. Let’s take control of your finances together!

    Best regards,  
    The EXPENSIFY Team  
    Taking the hassle out of expense tracking, one entry at a time.
    """

    message = MIMEMultipart()
    message['From'] = senderEmail
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(senderEmail, senderPassword)
            server.send_message(message)
            print("\nEmail Sent Successfully!\n")
    except Exception as e:
        print(f"Error Sending Welcome email: {e}")

def showDashboard(email):
    while True:
        print("\n--------------------")
        print("DASHBOARD".center(21))
        print("--------------------")
        dashboardSelect = input("[1] - TOTAL EXPENSES \n[2] - ADD EXPENSE \n[3] - EDIT EXPENSE \n[4] - DELETE EXPENSE \n[5] - EXIT \n-------------------- \nSelect here: ")
        if dashboardSelect == '1':
            viewTotalExpenses(email)
        elif dashboardSelect == '2':
            addExpense(email)
        elif dashboardSelect == '3':
            editExpense(email)
        elif dashboardSelect == '4':
            deleteExpense(email)
        elif dashboardSelect == '5':
            exitProgram()
        else:
            print("\nInvalid Option. Please Select a Valid Option.")

        if not returnToDashboard():
            break

def viewTotalExpenses(email):
    print("\n--------------------")
    print("TOTAL EXPENSES".center(20))
    print("--------------------")
    
    if email not in expenses or not expenses[email]:
        print("No Expenses Recorded.")
        return
    
    totalExpenses = sum(expenses[email].values())
    print(f"Total Expenses: ${totalExpenses:.2f}")
    
    print("\nExpenses by Category: \n---------------------")
    for category, amount in expenses[email].items():
        print(f"{category}: ${amount:.2f}")
    
    sendViaEmail = input("\nWould You Like A Copy Of Your Expenses Via Email? \n------------------------------------------------- \n[Yes] or [No]: ").lower()
    if sendViaEmail in ["yes", "y"]:
        sendExpensesViaEmail(email)

def sendExpensesViaEmail(email):
    recipient = email
    senderEmail = email
    senderPassword = input("\nApp Password for Email: ")

    subject = "Your Expense Tracker Summary"
    body = "Here are your Recorded Expenses:\n\n"

    for category, amount in expenses[email].items():
        body += f"{category}: ${amount:.2f}\n"

    message = MIMEMultipart()
    message['From'] = senderEmail
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(senderEmail, senderPassword)
            server.send_message(message)
            print("\nExpenses Sent Successfully!\n")
    except Exception as e:
        print(f"Error Sending Email: {e}")

def addExpense(email):
    category = input("\nCategory: ")
    expense = float(input("Amount Spent: "))
    
    if email in expenses:
        expenses[email][category] = expenses[email].get(category, 0) + expense
    else:
        expenses[email] = {category: expense}

    print(f"\nExpense Added: ${expense:.2f} in Category '{category}'.")
    saveExpenses()

def editExpense(email):
    print("\n--------------------")
    print("EDIT EXPENSES".center(21))
    print("--------------------")
    if email not in expenses or not expenses[email]:
        print("No Expenses Recorded.")
        return

    print("\nAvailable Categories:")
    for category in expenses[email]:
        print(f"- {category}")
    
    category = input("\nSelect Category: ")
    
    if category not in expenses[email]:
        print(f"No Expenses Found in Category '{category}'.")
        return
    
    newAmount = float(input("New Amount: "))
    expenses[email][category] = newAmount
    print(f"Expense Epdated: {category} = ${newAmount:.2f}")
    saveExpenses()

def deleteExpense(email):
    print("\n--------------------")
    print("DELETE EXPENSES".center(21))
    print("--------------------")
    
    if email not in expenses or not expenses[email]:
        print("No Expenses Recorded.")
        return
    
    print("\nAvailable Categories:")
    for category in expenses[email]:
        print(f"- {category}")
    
    category = input("\nSelect Category: ")
    
    if category not in expenses[email]:
        print(f"No Expenses Found in Category '{category}'.")
        return
    
    del expenses[email][category]
    print(f"Category '{category}' Deleted.")
    saveExpenses()

def returnToDashboard():
    while True:
        choice = input("\nBack to Dashboard? \n------------------ \n[Yes] or [No]: ").lower()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            exitProgram()
        else:
            print("\nInvalid input. Please enter 'Yes' or 'No'.")

def exitProgram():
    print("\n------------------------------------------------------------")
    print("|               Thank you for using EXPENSIFY!             |".center(60))
    print("------------------------------------------------------------")
    sys.exit()