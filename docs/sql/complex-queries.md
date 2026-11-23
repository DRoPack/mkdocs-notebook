# Complex Queries

## Subqueries

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A subquery is a query nested inside another query, often used in the `WHERE` clause to compare against a computed value.

    ---

    === "MongoDB"

        ```javascript
        // no nested-query syntax; resolve the computed value first, then filter
        const avgSalary = db.employees.aggregate([
            { $group: { _id: null, avg: { $avg: "$salary" } } }
        ]).next().avg;

        db.employees.find({ salary: { $gt: avgSalary } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        USE sql_hr;

        SELECT *
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
        );
        ```

## IN Operator with a Subquery

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `IN`/`NOT IN` can compare a column against the result set of a subquery.

    ---

    === "MongoDB"

        ```javascript
        const orderedProductIds = db.order_items.distinct("product_id");
        db.products.find({ product_id: { $nin: orderedProductIds } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- sql_store
        SELECT *
        FROM products
        WHERE product_id NOT IN (
            SELECT DISTINCT product_id
            FROM order_items
        );
        ```

## Subqueries vs Joins

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Many results achievable with a subquery can also be achieved with a join — both approaches below return the same results. Query performance between the two is covered later.

    ---

    === "MongoDB"

        ```javascript
        // resolve ids first (subquery-equivalent)
        const invoicedClientIds = db.invoices.distinct("client_id");
        db.clients.find({ client_id: { $nin: invoicedClientIds } });

        // using $lookup (join-equivalent)
        db.clients.aggregate([
            { $lookup: { from: "invoices", localField: "client_id", foreignField: "client_id", as: "invoices" } },
            { $match: { invoices: { $size: 0 } } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- using a subquery
        SELECT *
        FROM clients
        WHERE client_id NOT IN (
            SELECT DISTINCT client_id
            FROM invoices
        );

        -- using a join
        SELECT *
        FROM clients
        LEFT JOIN invoices USING (client_id)
        WHERE invoice_id IS NULL;
        ```

### Example: Subquery vs Join

=== "MongoDB"

    ```javascript
    // resolve ids first (subquery-equivalent)
    const customerIds = db.order_items.aggregate([
        { $lookup: { from: "orders", localField: "order_id", foreignField: "order_id", as: "order" } },
        { $unwind: "$order" },
        { $match: { product_id: 3 } },
        { $group: { _id: "$order.customer_id" } }
    ]).toArray().map(r => r._id);

    db.customers.find({ customer_id: { $in: customerIds } });

    // using $lookup (join-equivalent)
    db.customers.aggregate([
        { $lookup: { from: "orders", localField: "customer_id", foreignField: "customer_id", as: "orders" } },
        { $unwind: "$orders" },
        { $lookup: { from: "order_items", localField: "orders.order_id", foreignField: "order_id", as: "order_items" } },
        { $unwind: "$order_items" },
        { $match: { "order_items.product_id": 3 } }
    ]);
    ```

=== "MSSQL / SQLite / MySQL"

    ```sql
    -- using a subquery
    SELECT
        c.customer_id,
        c.first_name,
        c.last_name
    FROM customers c
    WHERE customer_id IN (
        SELECT o.customer_id
        FROM order_items oi
        JOIN orders o USING (order_id)
        WHERE product_id = 3
    );

    -- using a join
    SELECT DISTINCT
        c.customer_id,
        c.first_name,
        c.last_name
    FROM customers c
    JOIN orders o USING (customer_id)
    JOIN order_items oi USING (order_id)
    WHERE oi.product_id = 3;
    ```

## ALL Keyword

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Compares a single column value against a range of values returned by a subquery — the condition must hold true for `ALL` of them.

    ---

    === "MongoDB"

        ```javascript
        // no ALL keyword; pre-compute the boundary value (here, a MAX) and compare against it
        const maxForClient3 = db.invoices.aggregate([
            { $match: { client_id: 3 } },
            { $group: { _id: null, max: { $max: "$invoice_total" } } }
        ]).next().max;

        db.invoices.find({ invoice_total: { $gt: maxForClient3 } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT *
        FROM invoices
        WHERE invoice_total > ALL (
            SELECT invoice_total
            FROM invoices
            WHERE client_id = 3
        );
        ```

## ANY Keyword

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `= ANY` is equivalent to `IN` — the condition must hold true for at least one value returned by the subquery.

    ---

    === "MongoDB"

        ```javascript
        const clientIds = db.invoices.aggregate([
            { $group: { _id: "$client_id", count: { $sum: 1 } } },
            { $match: { count: { $gte: 2 } } }
        ]).toArray().map(r => r._id);

        db.clients.find({ client_id: { $in: clientIds } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT *
        FROM clients
        WHERE client_id = ANY (
            SELECT client_id
            FROM invoices
            GROUP BY client_id
            HAVING COUNT(*) >= 2
        );
        ```

## Correlated Subqueries

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A correlated subquery references a column from the outer query, so it re-executes once per row of the outer query.

    ---

    === "MongoDB"

        ```javascript
        // a pipeline-style $lookup with "let" is the correlated-subquery equivalent
        db.employees.aggregate([
            { $lookup: {
                from: "employees",
                let: { officeId: "$office_id" },
                pipeline: [
                    { $match: { $expr: { $eq: ["$office_id", "$$officeId"] } } },
                    { $group: { _id: null, avg: { $avg: "$salary" } } }
                ],
                as: "office_avg"
            } },
            { $unwind: "$office_avg" },
            { $match: { $expr: { $gt: ["$salary", "$office_avg.avg"] } } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- select employees whose salary is above the average in their own office
        SELECT *
        FROM employees e
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
            WHERE office_id = e.office_id -- correlated: re-evaluated per employee
        );
        ```

## EXISTS Operator

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `EXISTS` checks whether a correlated subquery returns any rows. It's more efficient than `IN` on large data sets (1000+ rows).

    ---

    === "MongoDB"

        ```javascript
        // checks if a client_id from clients exists in invoices
        db.clients.aggregate([
            { $lookup: { from: "invoices", localField: "client_id", foreignField: "client_id", as: "invoices" } },
            { $match: { invoices: { $ne: [] } } }
        ]);

        // find products that have never been ordered
        db.products.aggregate([
            { $lookup: { from: "order_items", localField: "product_id", foreignField: "product_id", as: "orders" } },
            { $match: { orders: { $size: 0 } } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- checks if a client_id from clients exists in invoices
        SELECT *
        FROM clients c
        WHERE EXISTS (
            SELECT client_id
            FROM invoices
            WHERE client_id = c.client_id
        );

        -- find products that have never been ordered
        SELECT *
        FROM products p
        WHERE NOT EXISTS (
            SELECT product_id
            FROM order_items
            WHERE product_id = p.product_id
        );
        ```

## Subqueries in the SELECT Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A subquery can compute a value for each row in the `SELECT` list. MySQL uniquely allows referencing an earlier column alias later in the same `SELECT` list with `(SELECT alias)` — MSSQL and SQLite do not support this and require repeating the subquery or wrapping the query in a CTE/subquery instead.

    ---

    === "MongoDB"

        ```javascript
        // no correlated column aliasing; compute the value once and reuse the variable
        const avgInvoice = db.invoices.aggregate([
            { $group: { _id: null, avg: { $avg: "$invoice_total" } } }
        ]).next().avg;

        db.invoices.aggregate([
            { $addFields: {
                invoice_average: avgInvoice,
                difference: { $subtract: ["$invoice_total", avgInvoice] }
            } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT
            invoice_id,
            invoice_total,
            (SELECT AVG(invoice_total)
                FROM invoices) AS invoice_average,
            invoice_total - (SELECT invoice_average) AS difference -- MySQL-only alias reuse
        FROM invoices;
        ```

## Subqueries in the FROM Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A subquery in the `FROM` clause acts as a temporary in-memory table that can be filtered further. An alias is required. Reserve this for simple, one-off queries — prefer a `VIEW` for anything reused.

    ---

    === "MongoDB"

        ```javascript
        // pipelines are naturally composable; no special "subquery in FROM" syntax is needed
        db.clients.aggregate([
            { $lookup: { from: "invoices", localField: "client_id", foreignField: "client_id", as: "invoices" } },
            { $addFields: {
                total_sales: { $sum: "$invoices.invoice_total" },
                average: { $avg: "$invoices.invoice_total" }
            } },
            { $match: { total_sales: { $ne: null } } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT *
        FROM (
            SELECT
                client_id,
                name,
                (SELECT SUM(invoice_total)
                    FROM invoices
                    WHERE client_id = c.client_id) AS total_sales,
                (SELECT AVG(invoice_total) FROM invoices) AS average,
                (SELECT total_sales - average) AS difference
            FROM clients c
        ) AS sales_summary -- alias required when using a subquery in FROM
        WHERE total_sales IS NOT NULL;
        ```
