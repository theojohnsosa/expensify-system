import sys
import re
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data():
    with open('user_data.json', 'w') as file:
        json.dump(user_data, file, indent=4)

def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_expenses():
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file, indent=4)

user_data = load_user_data()
expenses = load_expenses()

def is_valid_password(password):
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
        entry_input = input("[Sign In] – [Sign Up] - [Exit] \nSelect here: ")
        if entry_input.lower() == "sign in":
            sign_in()
        elif entry_input.lower() == "sign up":
            sign_up()
        elif entry_input.lower() == "exit":
            exit_program()
        else:
            print("\nInvalid Input. Please try again.\n")

def sign_in():
    while True:
        email_input = input("\nEmail: ")
        if email_input in user_data:
            forgot_password = input("[1] - Proceed or [2] - Forgot Password? \nSelect here: ")
            if forgot_password == "1":
                password_input = input("Password: ")
                if password_input == user_data[email_input]["password"]:
                    print(f"\nHello, {user_data[email_input]['username']}!")
                    show_dashboard(email_input)
                    return
                else:
                    print("\nIncorrect Password. Try Again.")
            elif forgot_password == "2":
                send_password_via_email(email_input)
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
                    exit_program()
                else:
                    print("\nInvalid Input. Please try again.")
            
def send_password_via_email(email):
    recipient = email
    sender_email = email
    sender_password = input("\nApp Password for Email: ")

    subject = "Password Recovery"
    body = f"Hello {user_data[email]['username']},\n\nHere is your password for Expense Tracker: {user_data[email]['password']}\n\nPlease keep this information secure.\n"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("\nEmail Sent Successfully!\n")
    except Exception as e:
        print(f"Error Sending Email: {e}")
                
def sign_up():
    email_input = input("\nEnter your Email: ")
    if email_input in user_data:
        print("\nEmail Already Exists. Please Try Again.\n")
    else:
        username_input = input("Enter your Username: ")
        password_input = input("Enter your Password: ")
        confirm_password = input("Confirm Password: ")
        if password_input != confirm_password:
            print("\nPasswords Do Not match. Please Try Again.\n")
        elif not is_valid_password(password_input):
            print("\nPassword must contain at least 1 capital letter, 1 small letter, \n1 number, no special characters, and be at least 6 characters long.\n")
        else:
            user_data[email_input] = {"username": username_input, "password": password_input}
            save_user_data()
            print("\nAccount Created. You Can Now Sign In!\n")
            send_welcome_email(email_input, username_input)

def send_welcome_email(email, username):
    recipient = email
    sender_email = email
    sender_password = input("App Password for Email: ")

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
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("\nEmail Sent Successfully!\n")
    except Exception as e:
        print(f"Error Sending Welcome email: {e}")

def show_dashboard(email):
    while True:
        print("\n--------------------")
        print("DASHBOARD".center(21))
        print("--------------------")
        dashboard_select = input("[1] - TOTAL EXPENSES \n[2] - ADD EXPENSE \n[3] - EDIT EXPENSE \n[4] - DELETE EXPENSE \n[5] - EXIT \n-------------------- \nSelect here: ")
        if dashboard_select == '1':
            view_total_expenses(email)
        elif dashboard_select == '2':
            add_expense(email)
        elif dashboard_select == '3':
            edit_expense(email)
        elif dashboard_select == '4':
            delete_expense(email)
        elif dashboard_select == '5':
            exit_program()
        else:
            print("\nInvalid Option. Please Select a Valid Option.")

        if not return_to_dashboard():
            break

def view_total_expenses(email):
    print("\n--------------------")
    print("TOTAL EXPENSES".center(20))
    print("--------------------")
    
    if email not in expenses or not expenses[email]:
        print("No Expenses Recorded.")
        return
    
    total_expenses = sum(expenses[email].values())
    print(f"Total Expenses: ${total_expenses:.2f}")
    
    print("\nExpenses by Category: \n---------------------")
    for category, amount in expenses[email].items():
        print(f"{category}: ${amount:.2f}")
    
    send_via_email = input("\nWould You Like A Copy Of Your Expenses Via Email? \n------------------------------------------------- \n[Yes] or [No]: ").lower()
    if send_via_email in ["yes", "y"]:
        send_expenses_via_email(email)

def send_expenses_via_email(email):
    recipient = email
    sender_email = email
    sender_password = input("\nApp Password for Email: ")

    subject = "Your Expense Tracker Summary"
    body = "Here are your Recorded Expenses:\n\n"

    for category, amount in expenses[email].items():
        body += f"{category}: ${amount:.2f}\n"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("\nExpenses Sent Successfully!\n")
    except Exception as e:
        print(f"Error Sending Email: {e}")

def add_expense(email):
    category = input("\nCategory: ")
    expense = float(input("Amount Spent: "))
    
    if email in expenses:
        expenses[email][category] = expenses[email].get(category, 0) + expense
    else:
        expenses[email] = {category: expense}

    print(f"\nExpense Added: ${expense:.2f} in Category '{category}'.")
    save_expenses()

def edit_expense(email):
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
    
    new_amount = float(input("New Amount: "))
    expenses[email][category] = new_amount
    print(f"Expense Epdated: {category} = ${new_amount:.2f}")
    save_expenses()

def delete_expense(email):
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
    save_expenses()

def return_to_dashboard():
    while True:
        choice = input("\nBack to Dashboard? \n------------------ \n[Yes] or [No]: ").lower()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            exit_program()
        else:
            print("\nInvalid input. Please enter 'Yes' or 'No'.")

def exit_program():
    print("\n------------------------------------------------------------")
    print("|               Thank you for using EXPENSIFY!             |".center(60))
    print("------------------------------------------------------------")
    sys.exit()

if __name__ == "__main__":
    main()