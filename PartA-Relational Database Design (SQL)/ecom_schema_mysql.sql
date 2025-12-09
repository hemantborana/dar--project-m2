-- Disable foreign key checks for clean start
SET FOREIGN_KEY_CHECKS = 0; 

-- DROP tables if they exist to allow for fresh creation
DROP TABLE IF EXISTS OrderDetail;
DROP TABLE IF EXISTS `Order`; -- "Order" is a keyword in MySQL, so we must enclose it in backticks
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Category;

-- -----------------------------------------------------
-- Table: Category (3NF)
-- -----------------------------------------------------
CREATE TABLE Category (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY, -- Use AUTO_INCREMENT for MySQL
    CategoryName VARCHAR(100) NOT NULL UNIQUE,
    CategoryDescription TEXT
);

-- -----------------------------------------------------
-- Table: Product (3NF)
-- -----------------------------------------------------
CREATE TABLE Product (
    ProductID INT AUTO_INCREMENT PRIMARY KEY, -- Use AUTO_INCREMENT
    ProductName VARCHAR(255) NOT NULL,
    SKU VARCHAR(50) UNIQUE NOT NULL,
    Price DECIMAL(10, 2) NOT NULL CHECK (Price > 0),
    StockQuantity INT NOT NULL CHECK (StockQuantity >= 0),
    CategoryID INT NOT NULL,
    
    -- Foreign Key Constraint
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
);

-- -----------------------------------------------------
-- Table: Customer (3NF)
-- -----------------------------------------------------
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY, -- Use AUTO_INCREMENT
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Phone VARCHAR(20),
    StreetAddress VARCHAR(255),
    City VARCHAR(100),
    StateProvince VARCHAR(100),
    PostalCode VARCHAR(20)
);

-- -----------------------------------------------------
-- Table: Order (3NF)
-- Must use backticks as "Order" is a reserved word
-- -----------------------------------------------------
CREATE TABLE `Order` ( 
    OrderID INT AUTO_INCREMENT PRIMARY KEY, -- Use AUTO_INCREMENT
    CustomerID INT NOT NULL,
    OrderDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10, 2) NOT NULL CHECK (TotalAmount >= 0),
    OrderStatus VARCHAR(50) NOT NULL DEFAULT 'Pending',
    
    -- Foreign Key Constraint
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- -----------------------------------------------------
-- Table: OrderDetail (3NF)
-- -----------------------------------------------------
CREATE TABLE OrderDetail (
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(10, 2) NOT NULL,
    
    -- Primary Key (Composite Key) and Foreign Key Constraints
    PRIMARY KEY (OrderID, ProductID),
    FOREIGN KEY (OrderID) REFERENCES `Order`(OrderID), -- Referencing the aliased table
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Data Seeding 

INSERT INTO Category (CategoryName, CategoryDescription) VALUES
('Electronics', 'Modern gadgets and devices.'),
('Apparel', 'Clothing and accessories.'),
('Books', 'Fiction and non-fiction titles.');

INSERT INTO Product (ProductName, SKU, Price, StockQuantity, CategoryID) VALUES
('Laptop Pro X', 'LPX-2025', 1200.00, 50, 1),
('Wireless Headphones', 'WH-A45', 75.00, 150, 1),
('T-Shirt Vintage', 'TS-V01', 25.00, 300, 2),
('Novel: The Data Alchemist', 'N-DA-01', 15.00, 100, 3),
('Smart Watch 2.0', 'SW-20', 150.00, 80, 1),
('Jeans Slim Fit', 'JF-SF', 55.00, 120, 2);

INSERT INTO Customer (FirstName, LastName, Email, Phone) VALUES
('Alice', 'Smith', 'alice.s@example.com', '555-1234'),
('Bob', 'Johnson', 'bob.j@example.com', '555-5678'),
('Charlie', 'Brown', 'charlie.b@example.com', '555-9012');

INSERT INTO `Order` (CustomerID, TotalAmount, OrderStatus) VALUES
(1, 1275.00, 'Shipped'), -- Alice's Order 1
(2, 25.00, 'Pending'),   -- Bob's Order 1
(1, 150.00, 'Delivered'), -- Alice's Order 2
(3, 15.00, 'Shipped');   -- Charlie's Order 1

INSERT INTO OrderDetail (OrderID, ProductID, Quantity, UnitPrice) VALUES
(1, 1, 1, 1200.00), 
(1, 2, 1, 75.00),   
(2, 3, 1, 25.00),   
(3, 5, 1, 150.00),   
(4, 4, 1, 15.00),    
(1, 2, 1, 75.00);