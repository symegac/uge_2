import mysql.connector
import getpass
import pandas as pd
import matplotlib.pyplot as plt

# Forbind til databasen
# En lille login-skærm for sjov
print("Du forsøger at logge ind i Northwind Server")
print("(indtast '\\q' for at afslutte)")
while True:
    username = input("Brugernavn: ")
    if username == "\\q": quit()

    password = getpass.getpass("Adgangskode: ")
    if password == "\\q": quit()

    try:
        connection = mysql.connector.connect(
            user=username, password=password,
            host="localhost", database="northwind"
        )
    except mysql.connector.Error as err:
        print("Kunne ikke forbinde til serveren.\nFejl: ", err)
        print("Prøv igen, eller indtast '\\q' for at afslutte.")
    except:
        print("Ukendt fejl. Prøv igen, eller indtast '\\q' for at afslutte.")
    else:
        print("SUCCES: Forbundet til serveren.")
        break

# Henter de tre nødvendige tabeller joined
select_query = """
SELECT * FROM orderdetails
JOIN orders
    ON orderdetails.OrderID = orders.OrderID
JOIN customers
    ON orders.CustomerID = customers.CustomerID;
"""

# Alternativt kan man bare analysere direkte med queriet:
# # country_sales_query = """
# # SELECT
# #     customers.Country AS Country,
# #     SUM(orderdetails.Quantity * orderdetails.UnitPrice) AS "Total Sales"
# # FROM orderdetails
# # JOIN orders
# #     ON orderdetails.OrderID = orders.OrderID
# # JOIN customers
# #     ON orders.CustomerID = customers.CustomerID
# # GROUP BY Country;
# # """

# Load data i Pandas
sales_data = pd.read_sql(select_query, connection)
# Alternativ måde at få dataene til pandas
# # with connection.cursor() as cursor:
# #     cursor.execute(select_query)
# #     rows = cursor.fetchall()
# # sales_data = pd.DataFrame(rows)

# Husk at lukke forbindelsen igen bagefter
connection.close()

# Ny kolonne til totalt salg for hver ordre
sales_data["Total Sales"] = sales_data["Quantity"] * sales_data["UnitPrice"]
# Selecter kolonnerne 'Country' og 'Total Sales' og grupperer efter land
country_sales = sales_data[["Country", "Total Sales"]].groupby("Country")
# Summerer alle salg og finder dermed det totale salg
total_country_sales = country_sales["Total Sales"].sum()

# Plotter dataene i søjlediagram
total_country_sales.plot.bar(
    title="Total sales by country",
    xlabel="Country",
    ylabel="Total sales (in USD)"
)
# Lidt formattering
plt.gca().yaxis.minorticks_on()
plt.gca().set_axisbelow(True)
plt.grid(True, "both", 'y')
plt.show()