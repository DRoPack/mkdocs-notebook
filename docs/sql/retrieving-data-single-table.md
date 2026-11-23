# Retrieving Data from a Single Table

## SELECT Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: The `SELECT` clause specifies which columns to return from a table.

    ---

    === "MongoDB"

        ```javascript
        // all fields
        db.customers.find({});

        // only specific fields
        db.customers.find({}, { first_name: 1, last_name: 1 });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- all columns
        SELECT *
        FROM customers;

        -- only specific columns
        SELECT first_name, last_name
        FROM customers;
        ```

### Column Aliases

Use `AS` to rename a column in the result set. Wrap the alias in quotes if it contains spaces.

=== "MSSQL"

    ```sql
    SELECT
        first_name AS FirstName,
        last_name AS [Last Name]
    FROM customers;
    ```

=== "MongoDB"

    ```javascript
    db.customers.aggregate([
        { $project: { FirstName: "$first_name", "Last Name": "$last_name" } }
    ]);
    ```

=== "SQLite / MySQL"

    ```sql
    SELECT
        first_name AS FirstName,
        last_name AS 'Last Name'
    FROM customers;
    ```

### Calculated Columns

Calculations can be performed directly in the `SELECT` statement (standard order of mathematical operations applies).

=== "MongoDB"

    ```javascript
    db.customers.aggregate([
        { $project: {
            first_name: 1,
            points: 1,
            total: { $add: [{ $multiply: ["$points", 10] }, 100] }
        } }
    ]);
    ```

=== "MSSQL / SQLite / MySQL"

    ```sql
    SELECT
        first_name,
        points,
        points * 10 + 100
    FROM customers;
    ```

### DISTINCT

Use `DISTINCT` to filter out duplicate values.

=== "MongoDB"

    ```javascript
    db.customers.distinct("state");
    ```

=== "MSSQL / SQLite / MySQL"

    ```sql
    SELECT DISTINCT state
    FROM customers;
    ```

## WHERE Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: The `WHERE` clause filters rows based on a condition. Supported operators: `>`, `>=`, `<`, `<=`, `=`, `!=`/`<>`.

    ---

    === "MongoDB"

        ```javascript
        // numeric comparison
        db.customers.find({ points: { $gt: 3000 } });

        // string equality
        db.customers.find({ state: "VA" });

        // date comparison
        db.customers.find({ birth_date: { $gt: ISODate("1990-01-01") } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- numeric comparison
        SELECT *
        FROM customers
        WHERE points > 3000;

        -- strings are enclosed in quotes
        SELECT *
        FROM customers
        WHERE state = 'VA';

        -- dates are enclosed in quotes as well
        SELECT *
        FROM customers
        WHERE birth_date > '1990-01-01';
        ```

## AND, OR, and NOT Operators

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Combine multiple conditions. `AND` has higher precedence than `OR`, so use parentheses to control order of evaluation.

    ---

    === "MongoDB"

        ```javascript
        // combine with $and / $or
        db.customers.find({
            $or: [
                { birth_date: { $gt: ISODate("1990-01-01") } },
                { $and: [{ points: { $gt: 1000 } }, { state: "VA" }] }
            ]
        });

        // use $not to reverse a condition
        db.customers.find({ points: { $not: { $gt: 1000 } } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- AND has higher precedence than OR
        SELECT *
        FROM customers
        WHERE birth_date > '1990-01-01' OR points > 1000 AND state = 'VA';

        -- use parenthesis to change the order
        SELECT *
        FROM customers
        WHERE (birth_date > '1990-01-01' OR points > 1000) AND state = 'VA';

        -- use NOT to reverse a statement
        SELECT *
        FROM customers
        WHERE NOT (birth_date > '1990-01-01' OR points > 1000);
        ```

## IN Operator

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Search for multiple values without writing several `OR` conditions. More efficient than an equivalent chain of `OR` statements.

    ---

    === "MongoDB"

        ```javascript
        // search for multiple values
        db.customers.find({ state: { $in: ["VA", "FL", "GA"] } });

        // inverse the search
        db.customers.find({ state: { $nin: ["VA", "FL", "GA"] } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- search for multiple values
        SELECT *
        FROM customers
        WHERE state IN ('VA', 'FL', 'GA');

        -- same as WHERE state = 'VA' OR state = 'FL' OR state = 'GA'
        -- but IN is a more efficient way to write it

        -- inverse the search
        SELECT *
        FROM customers
        WHERE state NOT IN ('VA', 'FL', 'GA');
        ```

## BETWEEN Operator

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Get values within a range (inclusive on both ends).

    ---

    === "MongoDB"

        ```javascript
        // no BETWEEN keyword; combine $gte and $lte
        db.customers.find({ points: { $gte: 1000, $lte: 3000 } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- get a range of values
        SELECT *
        FROM customers
        WHERE points BETWEEN 1000 AND 3000;

        -- same as WHERE points >= 1000 AND points <= 3000
        ```

## LIKE Operator

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Matches a pattern using the `%` wildcard.

    ---

    === "MongoDB"

        ```javascript
        // no LIKE keyword; use $regex instead
        db.customers.find({ last_name: { $regex: "^b", $options: "i" } }); // starts with 'b'
        db.customers.find({ last_name: { $regex: "b$", $options: "i" } }); // ends with 'b'
        db.customers.find({ last_name: { $regex: "b", $options: "i" } });  // contains 'b'
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- starts with 'b'
        SELECT *
        FROM customers
        WHERE last_name LIKE 'b%';

        -- ends with 'b'
        SELECT *
        FROM customers
        WHERE last_name LIKE '%b';

        -- contains 'b'
        SELECT *
        FROM customers
        WHERE last_name LIKE '%b%';
        ```

## IS NULL

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Check whether a column has a `NULL` value.

    ---

    === "MongoDB"

        ```javascript
        db.customers.find({ phone: null });
        db.customers.find({ phone: { $ne: null } });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT *
        FROM customers
        WHERE phone IS NULL;

        SELECT *
        FROM customers
        WHERE phone IS NOT NULL;
        ```

## ORDER BY

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Sort the result set by one or more columns, optionally in descending order or by a calculated expression.

    ---

    === "MongoDB"

        ```javascript
        db.customers.find().sort({ first_name: 1 });

        // descending order
        db.customers.find().sort({ first_name: -1 });

        // sort by multiple fields
        db.customers.find().sort({ state: 1, first_name: 1 });

        // sorting by a calculated expression requires an aggregation pipeline
        db.order_items.aggregate([
            { $addFields: { line_total: { $multiply: ["$quantity", "$unit_price"] } } },
            { $sort: { line_total: 1 } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        SELECT *
        FROM customers
        ORDER BY first_name;

        -- descending order
        SELECT *
        FROM customers
        ORDER BY first_name DESC;

        -- sort by multiple columns
        SELECT *
        FROM customers
        ORDER BY state, first_name;

        -- sort by a calculation of two columns
        SELECT *
        FROM order_items
        ORDER BY quantity * unit_price;
        ```

## Limiting Results

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Limit the number of rows returned, and optionally skip a number of rows first (useful for pagination).

    ---

    === "MSSQL"

        ```sql
        -- returns only the first 3 records
        SELECT TOP 3 *
        FROM customers;

        -- offset: skip first 6 records, then return next 3
        SELECT *
        FROM customers
        ORDER BY customer_id
        OFFSET 6 ROWS FETCH NEXT 3 ROWS ONLY;
        ```

    === "MongoDB"

        ```javascript
        // returns only the first 3 documents
        db.customers.find().limit(3);

        // offset: skip first 6 documents, then return next 3
        db.customers.find().skip(6).limit(3);
        ```

    === "SQLite / MySQL"

        ```sql
        -- returns only the first 3 records
        SELECT *
        FROM customers
        LIMIT 3;

        -- offset: skip first 6 records, then return next 3
        SELECT *
        FROM customers
        LIMIT 6, 3;
        ```
