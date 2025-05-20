-- This query calculates total sales for a specific customer segment.
-- It will be slower if there's no index on CustomerSegment.
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
