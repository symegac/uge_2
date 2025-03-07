-- Del 2: Grundlæggende dataudtræk
-- #2.2
SELECT * FROM Products
ORDER BY UnitPrice DESC;

-- #2.3
SELECT * FROM Customers
WHERE Country IN ("UK", "Spain");
-- Giver 12 rækker ☑

-- #2.4
SELECT * FROM Products
WHERE UnitsInStock > 100
	AND UnitPrice >= 25;
-- Giver 2 rækker, ikke 10. Har værdierne ændret sig?

-- #2.5
SELECT DISTINCT ShipCountry FROM Orders;
-- Giver 21 rækker ☑

-- #2.6
SELECT * FROM Orders
WHERE OrderDate LIKE "1996-10%";
-- Giver 26 rækker ☑ 

-- #2.7
SELECT * FROM Orders
WHERE ShipRegion IS NULL
	AND ShipCountry = "Germany"
    AND Freight >= 100
    AND EmployeeID = 1
    AND OrderDate LIKE "1996%";
-- Giver 2 rækker ☑

-- #2.8
SELECT * FROM Orders
WHERE ShippedDate > RequiredDate;
-- Giver 37 rækker ☑

-- #2.9
SELECT * FROM Orders
WHERE OrderDate BETWEEN "1997-01-01" AND "1997-04-30"
	AND ShipCountry = "Canada";
-- Giver 8 rækker ☑

-- #2.10
SELECT * FROM Orders
WHERE EmployeeID IN (2,5,8)
	AND ShipRegion IS NOT NULL
    AND ShipVia IN (1,3)
ORDER BY EmployeeID ASC, ShipVia ASC;
-- Giver 57 rækker ☑

-- #2.11
-- Der er ikke nogen ReportsTo-kolonne, har databasens struktur ændret sig siden opgaven oprindeligt blev skrevet?
-- Men ellers ville det være (Region IS NULL OR ReportsTo IS NULL)
SELECT * FROM Employees
WHERE Region IS NULL
    AND BirthDate <= "1960-12-31";
-- Giver 2 rækker (ikke 3)