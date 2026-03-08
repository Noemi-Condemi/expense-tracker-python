import datetime
import os
from datetime import datetime


DATA_FILE = "transactions.txt"
BUDGET_FILE = "budget.txt"

def load_transactions():
    """Load all the transactions from the file"""
    transactions = []
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE,"r") as file:
        for line in file:
            line= line.strip()

            if line:
                parts = line.split("|")
                if len(parts) == 4:
                    transaction = {
                        'date' : parts[0],
                        'type' : parts[1],
                        'category' : parts[2],
                        'amount': float(parts[3].strip()),
                    }
                    transactions.append(transaction)

    return transactions

# save_transaction and capture the date/time 

def save_transactions(transaction_type, category, amount):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    with open(DATA_FILE, "a") as file:
        file.write(f"{date}|{transaction_type}|{category}|{amount:.2f}\n")
       
    print(f" {transaction_type.capitalize()} of £{amount:,.2f} recorded successfully")
    

# **Add Income** - Record money you receive

def add_income():
    """Add a new income transaction"""
    print("\n ------Add Income------")
    category = input("Category (eg., Salary, Freelance, Gift)").strip().lower()
    
    while True:
        try: 
            amount = float(input("Enter an ammount: £"))
            if amount <= 0:
                print("Amount must be postive")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number") 
        
    save_transactions("income", category, amount)
        

# **Add Expense** - Record money you spend
    # ask user to enter an amount
    # check if the amount is positive

def add_expense():
    """Add a new expense transaction"""
    print("\n ------Add Expense------")
    category = input("Category (eg., Salary, Freelance, Gift)").strip().lower()
    while True:
        try: 
            amount = float(input("Enter an ammount: £"))
            if amount <= 0:
                print("Amount must be postive")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number") 
    
    save_transactions("expense", category, amount)
    

# **View All Transactions** - See your complete history
    
def view_all_transactions():
    transactions = load_transactions()
    if  not transactions:
        print("\n No Transactions found.")
        return
    
    print("\n" + "=" *70)
    print(f"{'Date':<20}{'Type':<10}{'Category':<20}{'Amount':>11}")
    
    for transaction in transactions:
        amount_str = f"£{transaction['amount']:.2f}"
        print(f"{transaction['date']:<20}{transaction['type'].capitalize():<10} {transaction['category'].capitalize():<20}{amount_str:>10}")
    
    print("="*70)

# **View by Category** - Group expenses by type

def view_by_category():
    """Shows by Category"""

    print("\n ------Enter Category------")
    category = input("Category (eg., Salary, Freelance, Gift)").strip().lower()
   
    transactions = load_transactions()
    counter = 0

    for transaction in transactions:
        if transaction['category'].lower() == category:
                print(f"{transaction['date']:<20}{transaction['type'].capitalize():<10}{transaction['category'].capitalize():<20}£{transaction['amount']:.2f}")
                counter +=1
    if counter == 0:
        print("\n No Transactions found.")
    print("\n" + "=" *70)

# **Date Filtering** - View transactions from specific time periods    
    
def view_by_date():
    """Filter by Date"""
    print("\n ------Enter Start Date------") 

    counter = 0

    while True:
        try:
            start_input = input("Date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_input, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid format. Please enter YYYY-MM-DD")
            
    print("\n ------Enter End Date------")

    while True:
        try:
            end_input = input("Date (YYYY-MM-DD): ")
            end_date = datetime.strptime(end_input, "%Y-%m-%d")
            end_date = end_date.replace(hour=23, minute=59, second=59)
            break
        except ValueError:
            print("Invalid format. Please enter YYYY-MM-DD")            

    transactions = load_transactions()

    if  not transactions:
        print("\n No Transactions found.")
        return
    
    print("\n" + "=" *70)
 
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction['date'].strip(), "%Y-%m-%d %H:%M:%S") 

        if  start_date <= transaction_date <= end_date:
            print(f"{transaction['date']:<20}{transaction['type'].strip().lower().capitalize():<10} {transaction['category'].strip().lower().capitalize():<20}£{transaction['amount']:.2f}")
            counter +=1

    if counter == 0:
        print("\n No Transactions found.")

    print("\n" + "=" *70)



# **Set Budget** - Set a monthly spending limit

def set_budget():
    print("\n --- Set Monthly Budget ---")

    while True:
        try:
            budget = float(input("Enter monthly budget amount: "))
            if budget < 0:
                print("Budget cannot be negative. Try again")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number")

    with open(BUDGET_FILE, "w") as file:
        file.write(str(budget))

    print(f"Monthly Budget set to: £{budget:,.2f}")

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r") as file:
            try:
                return float(file.read().strip())
            except ValueError:
                return 0
    return 0
            
# **View Summary** - See total income, expenses, and balance

def calculate_summary():
    transactions = load_transactions()
    if  not transactions:
        print("\n No Transactions found.")
        return
    
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        if transaction['type'].lower().strip() == 'income':
            total_income += transaction["amount"]

        elif transaction['type'].strip() == 'expense':
            total_expenses += transaction["amount"]

    balance = total_income - total_expenses

    print("\n" + "="*50)
    print(f"Total Income: £{total_income:.2f}")
    print(f"Total Expenses: £{total_expenses:.2f}")
    print(f"Balance: £{balance:.2f}")

# **Clear Data** - Reset all transactions

def clear_all_data():
    confirm = input("Type 'DELETE' to confirm: ").strip()
    if confirm == 'DELETE':
        if os.path.exists(BUDGET_FILE):
            os.remove(BUDGET_FILE)
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        print("All the data has been cleared successfully.")
    else:
        print("Operation Cancelled")


#display menu

def display_menu():
    """This will display the list of options."""
    print("="*50)
    print("Personal Finance Tracker")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. View Summary")
    print("5. View by Category")
    print("6. View by Date")
    print("7. Set Monthly Budget")
    print("8. Clear All Data")
    print("9. Exit")
    print("="*50)



def main():
    print("\n Welcome to personal Finance Tracker")

    while True:
        display_menu()
        choice = input("\n Enter your choice (1 - 9) " )

        if choice =="1":
            add_income()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_all_transactions()
        elif choice == "4":
            calculate_summary()
        elif choice == "5":
            view_by_category()
        elif choice == "6":
            view_by_date()
        elif choice == "7":
            set_budget()
        elif choice == "8":
            clear_all_data()
        elif choice == "9":
            print("Thank you for using our system.")
            break
        else:
            print("Invalide choice. Please enter a number from 1 to 9.")
            

main()
