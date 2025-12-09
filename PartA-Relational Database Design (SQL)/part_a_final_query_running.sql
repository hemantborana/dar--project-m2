USE ecom_project;

-- Query 2
WITH ProductSales AS (
    -- Calculating the total quantity and revenue per product
    SELECT
        P.ProductID,
        P.ProductName,
        Cat.CategoryName,
        SUM(OD.Quantity) AS TotalQuantitySold,
        SUM(OD.Quantity * OD.UnitPrice) AS TotalRevenue
    FROM
        Product P
    JOIN
        OrderDetail OD ON P.ProductID = OD.ProductID
    JOIN
        Category Cat ON P.CategoryID = Cat.CategoryID
    GROUP BY
        P.ProductID, P.ProductName, Cat.CategoryName
)
SELECT
    CategoryName,
    ProductName,
    TotalRevenue,
    TotalQuantitySold,
    -- Window Function 1: Ranks products within their own category (partition)
    ROW_NUMBER() OVER (PARTITION BY CategoryName ORDER BY TotalQuantitySold DESC) AS RankInCategory,
    -- Window Function 2: Ranks all products globally by revenue
    RANK() OVER (ORDER BY TotalRevenue DESC) AS GlobalRevenueRank
FROM
    ProductSales
ORDER BY
    CategoryName, RankInCategory;
    
    
-- Query 3a: Subquery Example
-- Find customers whose total order amount is greater than the average of ALL orders
SELECT
    C.FirstName,
    C.LastName,
    O.TotalAmount
FROM
    Customer C
JOIN
    `Order` O ON C.CustomerID = O.CustomerID
WHERE
    O.TotalAmount > (SELECT AVG(TotalAmount) FROM `Order`);
    
    
-- Query 3b: FULL OUTER JOIN Simulation (Shows unmatched records)
(SELECT
    C.FirstName,
    NULL AS ProductName,
    O.OrderID
FROM
    Customer C
LEFT JOIN
    `Order` O ON C.CustomerID = O.CustomerID
WHERE O.OrderID IS NULL) 

UNION

(SELECT
    NULL AS FirstName,
    P.ProductName,
    NULL AS OrderID
FROM
    Product P
LEFT JOIN
    OrderDetail OD ON P.ProductID = OD.ProductID
WHERE OD.OrderID IS NULL);


-- Query 4:
DELIMITER ;

USE ecom_project;

-- Reset Stock to Initial Value
UPDATE Product SET StockQuantity = 50 WHERE ProductID = 1;

SET @ProductToUpdate = 1;
SET @OrderQuantity = 45;
SET @SafetyThreshold = 20;

-- 1. Display initial stock
SELECT CONCAT('Initial Stock: ', StockQuantity) AS Status FROM Product WHERE ProductID = @ProductToUpdate;

-- A. START TRANSACTION
START TRANSACTION;

-- B. Attempt the stock reduction
UPDATE Product
SET StockQuantity = StockQuantity - 45 -- Directly using 45 units
WHERE ProductID = 1;

-- C. Check the temporary stock level (MUST BE 5)
SELECT StockQuantity FROM Product WHERE ProductID = 1;

-- D. Execute the ROLLBACK command
ROLLBACK;

-- E. Final Stock Check
SELECT CONCAT('Final Stock: ', StockQuantity) AS Status FROM Product WHERE ProductID = 1;