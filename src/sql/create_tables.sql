DROP TABLE IF EXISTS Sales;

CREATE TABLE Sales (
    OrderID INTEGER PRIMARY KEY,
    ProductID TEXT NOT NULL,
    CustomerSegment TEXT,
    SaleDate TEXT, -- Using TEXT for simplicity, ideally DATE type
    Quantity INTEGER,
    UnitPrice REAL,
    Discount REAL,
    TotalSale REAL
);

-- No index on CustomerSegment initially to simulate a less optimized state
