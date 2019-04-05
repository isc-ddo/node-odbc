# PURPOSE: Add several portfolio items.
#
# NOTES: When running,
# 1. Choose option 1 to see list of stocks.
# 2. Choose option 2 to create portfolio.
# 3. Choose option 3 and add stocks using names from the previous list of stocks

import pyodbc
from datetime import datetime


# Find top 10 stocks on a particular date
def find_top_on_date(connection, date):
    cursor = connection.cursor()
    sql = "SELECT distinct top 10 transdate,name,stockclose,stockopen,high,low,volume FROM Demo.Stock " \
          "WHERE transdate = ? ORDER BY stockclose desc"
    print("Date\t\tName\tOpening Price\tDaily High\tDaily Low\tClosing Price\tVolume")

    rows = cursor.execute(sql, datetime.strptime(date, "%Y-%m-%d"))
    for row in rows:
        for item in row:
            print("{}\t".format(item), end='')
        print


# Create portfolio table
def create_portfolio_table(connection):
    cursor = connection.cursor()
    create_table = "CREATE TABLE Demo.Portfolio(Name varchar(50) unique, PurchaseDate date, " \
                   "PurchasePrice numeric(10,4), Shares int, DateTimeUpdated datetime)"
    try:
        cursor.execute(create_table)
        print("Created Demo.Portfolio table successfully.")
        connection.commit()
    except Exception as e:
        print("Error creating portfolio: " + str(e))


# Add item to portfolio
def add_portfolio_item(connection, name, purchase_date, price, shares):
    try:
        sql = "INSERT INTO Demo.Portfolio (name,PurchaseDate,PurchasePrice,Shares,DateTimeUpdated) VALUES (?,?,?,?,?)"
        stock_name = name.encode('utf-8')
        cursor = connection.cursor()
        purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
        current_time = datetime.now()
        cursor.execute(sql, stock_name, purchase_date, float(price), float(shares), current_time)
        print("Added new line item for stock: {}.".format(name))
        connection.commit()
    except Exception as e:
        print("Error adding to portfolio: " + str(e))


# Task 2: View top 10 stocks for selected date
# Note: Choose 2016/08/12 for date
def task2(connection):
    date = input("On which date? (YYYY-MM-DD) ")
    find_top_on_date(connection, date)


# Task 3: Create Portfolio Table
def task3(connection):
    print("Creating portfolio ...")
    create_portfolio_table(connection)


# Task 4: Add item to Portfolio table
# Note: Choose stock name using list of stocks generated by Task 2
def task4(connection):
    print("Add to portfolio")
    name = input("Name: ")
    date = input("Date: ")
    price = input("Price: ")
    shares = input("Number of shares: ")
    add_portfolio_item(connection, name, date, price, shares)


# Execute task based on user input
def execute_selection(selection, connection):
    if selection == 1:
        task2(connection)
    elif selection == 2:
        task3(connection)
    elif selection == 3:
        task4(connection)
    elif selection == 4:
        print("TO DO: Update Portfolio")
    elif selection == 5:
        print("TO DO: Delete from Portfolio")
    elif selection == 6:
        print("TO DO: View Portfolio")


# Get connection details from config file
def get_connection_info(file_name):
    # Initial empty dictionary to store connection details
    connections = {}

    # Open config file to get connection info
    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            # remove all white space (space, tab, new line)
            line = ''.join(line.split())

            # get connection info
            connection_param, connection_value = line.split(":")
            connections[connection_param] = connection_value
    return connections


def run():
    # Retrieve connection information from configuration file
    connection_detail = get_connection_info("connection.config")

    ip = connection_detail["ip"]
    port = int(connection_detail["port"])
    namespace = connection_detail["namespace"]
    username = connection_detail["username"]
    password = connection_detail["password"]
    driver = "{InterSystems ODBC}"

    # Create connection to InterSystems IRIS
    connection_string = 'DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}'\
        .format(driver, ip, port, namespace, username, password)

    connection = pyodbc.connect(connection_string)
    print("Connected to InterSystem IRIS")

    # Starting interactive prompt
    while True:
        print("1. View top 10")
        print("2. Create Portfolio table")
        print("3. Add to Portfolio")
        print("4. Update Portfolio")
        print("5. Delete from Portfolio")
        print("6. View Portfolio")
        print("7. Quit")
        selection = int(input("What would you like to do? "))
        if selection == 7:
            break
        elif selection not in range(1, 8):
            print("Invalid option. Try again!")
            continue
        execute_selection(selection, connection)


if __name__ == '__main__':
    run()

