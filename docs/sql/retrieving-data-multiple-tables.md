# Retrieving Data from Multiple Tables

## INNER JOIN

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Combines rows from two tables where a matching value exists in both. Only the `JOIN` keyword is needed (`INNER` is implied).

    ---

    === "MongoDB"

        ```javascript
        // $lookup is a LEFT JOIN by default; $match + $ne: [] filters out
        // documents with no matches, simulating an INNER JOIN
        db.orders.aggregate([
            { $lookup: { from: "customers", localField: "customer_id", foreignField: "customer_id", as: "customer" } },
            { $match: { customer: { $ne: [] } } },
            { $unwind: "$customer" }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- o and c are aliases of the tables, used for shortening later references
        SELECT *
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id;
        ```

## Joining Across Databases

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Prefix the table name with its database (and, on some engines, schema) name in the `JOIN` statement to join across databases.

    ---

    === "MSSQL"

        ```sql
        -- three-part name: database.schema.table
        SELECT *
        FROM order_items oi
        JOIN sql_inventory.dbo.products p
            ON oi.product_id = p.product_id;
        ```

    === "MongoDB"

        No direct equivalent:

        - `$lookup` only joins collections within the **same** database
        - Cross-database joins aren't supported natively — the workaround is to expose the other database's collection through a view, or read/merge the data in the application layer

    === "SQLite"

        ```sql
        -- attach the other database file first, then schema-qualify the table
        ATTACH DATABASE 'inventory.db' AS sql_inventory;

        SELECT *
        FROM order_items oi
        JOIN sql_inventory.products p
            ON oi.product_id = p.product_id;
        ```

    === "MySQL"

        ```sql
        SELECT *
        FROM order_items oi
        JOIN sql_inventory.products p
            ON oi.product_id = p.product_id;
        ```

## Self Joins

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Joins a table to itself, using different aliases to distinguish each reference.

    ---

    === "MongoDB"

        ```javascript
        // a collection can $lookup into itself using the same collection name
        db.employees.aggregate([
            { $lookup: { from: "employees", localField: "reports_to", foreignField: "employee_id", as: "manager" } },
            { $unwind: { path: "$manager", preserveNullAndEmptyArrays: true } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        USE sql_hr;

        -- e is alias for employees, m is alias for the same table representing the manager
        SELECT
            e.employee_id,
            e.first_name,
            m.first_name AS manager
        FROM employees e
        JOIN employees m
            ON e.reports_to = m.employee_id;
        ```

## Joining Multiple Tables

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Chain multiple `JOIN` clauses to combine more than two tables.

    ---

    === "MongoDB"

        ```javascript
        // chain multiple $lookup stages, one per related collection
        db.orders.aggregate([
            { $lookup: { from: "customers", localField: "customer_id", foreignField: "customer_id", as: "customer" } },
            { $lookup: { from: "order_statuses", localField: "status", foreignField: "order_status_id", as: "order_status" } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        USE sql_store;

        SELECT *
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN order_statuses os
            ON o.status = os.order_status_id;
        ```

## Compound Join Conditions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Join on more than one column using `AND` in the `ON` clause, typically needed when a table's primary key is composite.

    ---

    === "MongoDB"

        ```javascript
        // use a pipeline-style $lookup with $expr/$and to match on multiple fields
        db.order_items.aggregate([
            { $lookup: {
                from: "order_item_notes",
                let: { orderId: "$order_id", productId: "$product_id" },
                pipeline: [
                    { $match: { $expr: { $and: [
                        { $eq: ["$order_id", "$$orderId"] },
                        { $eq: ["$product_id", "$$productId"] }
                    ] } } }
                ],
                as: "notes"
            } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT *
        FROM order_items oi
        JOIN order_item_notes oin
            ON oi.order_id = oin.order_id
            AND oi.product_id = oin.product_id;
        ```

## Implicit Join Syntax

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Joining tables by listing them in the `FROM` clause and filtering in `WHERE`. **Not recommended** — prefer the explicit `JOIN ... ON` syntax.

    ---

    === "MongoDB"

        No direct equivalent:

        - There's no `FROM`-list/comma-join concept — every join is expressed explicitly as a `$lookup` stage

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- explicit join syntax (preferred)
        SELECT *
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id;

        -- implicit join syntax (not recommended)
        SELECT *
        FROM orders o, customers c
        WHERE o.customer_id = c.customer_id;
        ```

## Outer Joins

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `LEFT JOIN` returns all rows from the left table plus matches from the right table, including non-matches (`NULL` where no match exists). `RIGHT JOIN` does the same in reverse. **Best practice: avoid `RIGHT JOIN`**, use `LEFT JOIN` instead.

    ---

    === "MSSQL"

        No difference — same `LEFT JOIN`/`RIGHT JOIN` syntax as MySQL.

    === "MongoDB"

        - `$lookup` always behaves like a `LEFT JOIN` — there's no built-in `RIGHT JOIN` direction; swap which collection runs the aggregation to get the same result
        - MySQL has no `FULL OUTER JOIN`; MongoDB has no direct equivalent either — both require combining a left and a right result (via `UNION`/`$unionWith`)

        ```javascript
        db.customers.aggregate([
            { $lookup: { from: "orders", localField: "customer_id", foreignField: "customer_id", as: "orders" } },
            { $unwind: { path: "$orders", preserveNullAndEmptyArrays: true } }
        ]);
        ```

    === "SQLite"

        `RIGHT JOIN` and `FULL OUTER JOIN` require SQLite 3.39.0 (2022) or later; earlier versions only support `LEFT JOIN`.

    === "MySQL"

        No `FULL OUTER JOIN` — emulate it with a `UNION` of a `LEFT JOIN` and a `RIGHT JOIN`.

        ```sql
        -- returns all customers, even those without an order record
        SELECT
            c.customer_id,
            c.first_name,
            o.order_id
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
        ORDER BY c.customer_id;
        ```

## Outer Join Between Multiple Tables

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Chain multiple `LEFT JOIN` clauses to preserve unmatched rows across several tables.

    ---

    === "MongoDB"

        ```javascript
        // chain multiple $lookup + $unwind (preserving unmatched) stages
        db.customers.aggregate([
            { $lookup: { from: "orders", localField: "customer_id", foreignField: "customer_id", as: "orders" } },
            { $unwind: { path: "$orders", preserveNullAndEmptyArrays: true } },
            { $lookup: { from: "shippers", localField: "orders.shipper_id", foreignField: "shipper_id", as: "shipper" } },
            { $unwind: { path: "$shipper", preserveNullAndEmptyArrays: true } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT
            c.customer_id,
            c.first_name,
            o.order_id,
            sh.name AS Shipper
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id
        LEFT JOIN shippers sh
            ON o.shipper_id = sh.shipper_id
        ORDER BY c.customer_id;
        ```

## Self Outer Joins

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A `LEFT JOIN` of a table to itself, useful when related rows (e.g. a manager) may not exist.

    ---

    === "MongoDB"

        ```javascript
        // preserveNullAndEmptyArrays keeps employees with no manager
        db.employees.aggregate([
            { $lookup: { from: "employees", localField: "reports_to", foreignField: "employee_id", as: "manager" } },
            { $unwind: { path: "$manager", preserveNullAndEmptyArrays: true } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        USE sql_hr;

        SELECT
            e.employee_id,
            e.first_name,
            m.first_name AS Manager
        FROM employees e
        LEFT JOIN employees m
            ON e.reports_to = m.employee_id;
        ```

## USING Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `USING` can replace `ON` when the joined columns share the exact same name in both tables. It also accepts multiple columns for compound joins. **MSSQL does not support `USING`** — use `ON` instead.

    ---

    === "MSSQL"

        ```sql
        -- USING is not supported; use ON instead
        SELECT
            o.order_id,
            c.first_name,
            sh.name AS shipper
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        LEFT JOIN shippers sh
            ON o.shipper_id = sh.shipper_id;
        ```

    === "MongoDB"

        ```javascript
        // joins are expressed with $lookup, matching on field names directly
        db.orders.aggregate([
            { $lookup: { from: "customers", localField: "customer_id", foreignField: "customer_id", as: "customer" } }
        ]);
        ```

    === "SQLite / MySQL"

        ```sql
        SELECT
            o.order_id,
            c.first_name,
            sh.name AS shipper
        FROM orders o
        JOIN customers c
            -- ON o.customer_id = c.customer_id
            USING (customer_id)
        LEFT JOIN shippers sh
            USING (shipper_id);

        -- example joining on multiple columns
        SELECT *
        FROM order_items oi
        JOIN order_item_notes oin
            -- ON oi.order_id = oin.order_id AND oi.product_id = oin.product_id
            USING (order_id, product_id);
        ```

## Natural Joins

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Lets the DBMS automatically pick the column(s) to join on. **Not recommended** — the join column is implicit and can change unexpectedly if the schema changes. **MSSQL does not support `NATURAL JOIN`.**

    ---

    === "MSSQL"

        ```sql
        -- NATURAL JOIN is not supported; the join column(s) must be explicit
        SELECT
            o.order_id,
            c.first_name
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id;
        ```

    === "MongoDB"

        No direct equivalent:

        - `$lookup` has no "guess the join field" mode — `localField`/`foreignField` must always be spelled out explicitly
        - There's no schema-driven auto-join behavior to disable/enable, since MongoDB has no fixed schema to infer matching columns from

    === "SQLite / MySQL"

        ```sql
        SELECT
            o.order_id,
            c.first_name
        FROM orders o
        NATURAL JOIN customers c;
        ```

## Cross Joins

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Combines every row from one table with every row from another (Cartesian product).

    ---

    === "MongoDB"

        No native equivalent — the closest approximation is a `$lookup` with an empty pipeline (matches everything) followed by `$unwind`, but this is uncommon and inefficient at scale:

        ```javascript
        db.customers.aggregate([
            { $lookup: { from: "products", pipeline: [], as: "product" } },
            { $unwind: "$product" }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        USE sql_store;

        SELECT
            c.first_name AS customer,
            p.name AS product
        FROM customers c
        CROSS JOIN products p
        ORDER BY c.first_name;
        ```

## Unions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `UNION` stacks rows from several queries (vs. `JOIN`, which combines columns from several tables). Each query must select the same number of columns. A literal string value can be used to tag which query a row came from.

    ---

    === "MongoDB"

        ```javascript
        // the aggregation equivalent is $unionWith
        db.customers.aggregate([
            { $match: { points: { $gte: 3000 } } },
            { $addFields: { type: "Gold" } },
            { $unionWith: {
                coll: "customers",
                pipeline: [
                    { $match: { points: { $gte: 2000, $lte: 3000 } } },
                    { $addFields: { type: "Silver" } }
                ]
            } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT
            customer_id,
            first_name,
            points,
            'Gold' AS type -- literal string
        FROM customers
        WHERE points >= 3000

        UNION

        SELECT
            customer_id,
            first_name,
            points,
            'Silver' AS type
        FROM customers
        WHERE points BETWEEN 2000 AND 3000

        UNION

        SELECT
            customer_id,
            first_name,
            points,
            'Bronze' AS type
        FROM customers
        WHERE points <= 2000
        ORDER BY first_name;
        ```
