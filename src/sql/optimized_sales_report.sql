-- This query is the same as slow_sales_report.sql.
-- The performance improvement comes from an index on CustomerSegment.
SELECT
    CustomerSegment,
    SUM(TotalSale) as TotalSalesAmount,
    AVG(Quantity) as AverageQuantity,
    COUNT(OrderID) as NumberOfOrders
FROM
    Sales
WHERE
    CustomerSegment = ? -- Parameter for customer segment
GROUP BY
    CustomerSegment;
