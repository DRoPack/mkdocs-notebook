# Summarizing Data

## Aggregate Functions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Aggregate functions compute a single value across a set of rows. `COUNT(column)` ignores `NULL` values, while `COUNT(*)` counts every row regardless of `NULL`s.

    ---

    === "MongoDB"

        ```javascript
        db.invoices.aggregate([
            { $group: {
                _id: null,
                highest: { $max: "$invoice_total" },
                lowest: { $min: "$invoice_total" },
                average: { $avg: "$invoice_total" },
                sum: { $sum: "$invoice_total" },
                number_of_invoices: { $sum: { $cond: [{ $ne: ["$invoice_total", null] }, 1, 0] } },
                count_of_payments: { $sum: { $cond: [{ $ne: ["$payment_date", null] }, 1, 0] } },
                total_records: { $sum: 1 }
            } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT
            MAX(invoice_total) AS highest,
            MIN(invoice_total) AS lowest,
            AVG(invoice_total) AS average,
            SUM(invoice_total) AS sum,
            COUNT(invoice_total) AS number_of_invoices,
            COUNT(payment_date) AS count_of_payments, -- ignores NULL values
            COUNT(*) AS total_records -- total number of records in the table
        FROM invoices;
        ```

### With DISTINCT and WHERE

```sql
SELECT
    MAX(invoice_total) AS highest,
    MIN(invoice_total) AS lowest,
    AVG(invoice_total) AS average,
    SUM(invoice_total) AS sum,
    COUNT(DISTINCT client_id) AS total_records -- count of distinct clients
FROM invoices
WHERE invoice_date > '2019-07-01';
```

### Combining with UNION

A literal string can label each result set when combining aggregate queries with `UNION`.

```sql
SELECT
    'First half of 2019' AS date_range,
    SUM(invoice_total) AS total_sales,
    SUM(payment_total) AS total_payments,
    SUM(invoice_total - payment_total) AS what_we_expect
FROM invoices
WHERE invoice_date BETWEEN '2019-01-01' AND '2019-06-30'

UNION

SELECT
    'Second half of 2019' AS date_range,
    SUM(invoice_total) AS total_sales,
    SUM(payment_total) AS total_payments,
    SUM(invoice_total - payment_total) AS what_we_expect
FROM invoices
WHERE invoice_date BETWEEN '2019-07-01' AND '2019-12-31'

UNION

SELECT
    'Total' AS date_range,
    SUM(invoice_total) AS total_sales,
    SUM(payment_total) AS total_payments,
    SUM(invoice_total - payment_total) AS what_we_expect
FROM invoices
WHERE invoice_date BETWEEN '2019-01-01' AND '2019-12-31';
```

## GROUP BY Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Groups rows sharing the same value(s) so aggregate functions can be applied per group.

    ---

    === "MongoDB"

        ```javascript
        db.invoices.aggregate([
            { $match: { invoice_date: { $gte: ISODate("2019-07-01") } } },
            { $group: { _id: "$client_id", total_sales: { $sum: "$invoice_total" } } },
            { $sort: { total_sales: -1 } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT
            client_id,
            SUM(invoice_total) AS total_sales
        FROM invoices
        WHERE invoice_date >= '2019-07-01'
        GROUP BY client_id
        ORDER BY total_sales DESC;
        ```

### With a Join

```sql
SELECT
    date,
    pm.name AS payment_method,
    SUM(amount) AS total_payments
FROM payments p
JOIN payment_methods pm
    ON p.payment_method = pm.payment_method_id
GROUP BY date, payment_method
ORDER BY date;
```

## HAVING Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `WHERE` filters rows *before* grouping; `HAVING` filters groups *after* aggregation. Columns referenced in `HAVING` must appear in the `SELECT` list, unlike `WHERE`.

    ---

    === "MongoDB"

        ```javascript
        // HAVING has no direct keyword; add a $match stage after $group instead
        db.invoices.aggregate([
            { $group: { _id: "$client_id", total_sales: { $sum: "$invoice_total" } } },
            { $match: { total_sales: { $gt: 500 } } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT
            client_id,
            SUM(invoice_total) AS total_sales
        FROM invoices
        GROUP BY client_id
        HAVING total_sales > 500;

        SELECT
            client_id,
            SUM(invoice_total) AS total_sales,
            COUNT(*) AS number_of_invoices
        FROM invoices
        GROUP BY client_id
        HAVING total_sales > 500 AND number_of_invoices > 5;
        ```

### Exercise

```sql
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(oi.quantity * oi.unit_price) AS sales
FROM customers c
JOIN orders o
    USING (customer_id)
JOIN order_items oi
    USING (order_id)
WHERE state = 'VA'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
HAVING sales > 100;
```

## ROLLUP Operator

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `ROLLUP` adds subtotal and grand-total rows to grouped results. Only available when using aggregate functions. SQLite has no equivalent, and MongoDB requires a separate `$group` stage to compute totals.

    ---

    === "MSSQL"

        ```sql
        -- standard syntax (SQL:1999)
        SELECT
            state,
            city,
            SUM(invoice_total) AS total_sales
        FROM invoices i
        JOIN clients USING (client_id)
        GROUP BY ROLLUP (state, city);
        ```

    === "MongoDB"

        ```javascript
        // compute the grand total with a separate $group stage
        db.invoices.aggregate([
            { $group: { _id: { state: "$state", city: "$city" }, total_sales: { $sum: "$invoice_total" } } }
        ]);
        ```

    === "SQLite"

        No direct equivalent:

        - No `ROLLUP`, `CUBE`, or `GROUPING SETS` support
        - Subtotals/grand totals must be computed with separate queries combined via `UNION`

    === "MySQL"

        ```sql
        SELECT
            state,
            city,
            SUM(invoice_total) AS total_sales
        FROM invoices i
        JOIN clients USING (client_id)
        GROUP BY state, city WITH ROLLUP;

        SELECT
            pm.name AS payment_type,
            SUM(p.amount) AS total
        FROM payments p
        JOIN payment_methods pm
            ON p.payment_method = pm.payment_method_id
        GROUP BY pm.name WITH ROLLUP;
        ```
