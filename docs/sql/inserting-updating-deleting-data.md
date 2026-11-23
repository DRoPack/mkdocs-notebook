# Inserting, Updating, Deleting Data

## VARCHAR vs CHAR

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `VARCHAR(50)` uses only the amount of space needed to store the data. `CHAR(50)` always uses the full 50 characters regardless of the actual data length, padding with spaces to fill the remainder.

    ---

    === "MongoDB"

        No fixed-length string type — every string is stored as the single `string` BSON type (UTF-8), so there's no `VARCHAR`/`CHAR` distinction or padding behavior to consider.

    === "MSSQL / SQLite / MySQL"

        No difference — the same `VARCHAR`/`CHAR` distinction described above applies identically.

## Insert Row

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: When columns are not listed, every column must be accounted for in order, using `DEFAULT` or `NULL` where appropriate. When columns are listed, auto-increment or nullable-by-default columns can be excluded.

    ---

    === "MongoDB"

        ```javascript
        // no fixed column order or auto-increment key to account for;
        // _id (the primary key equivalent) is generated automatically
        db.customers.insertOne({
            first_name: "John",
            last_name: "Smith",
            birth_date: ISODate("1980-10-10"),
            phone: null,
            address: "1234 Acme Road",
            city: "Town",
            state: "FL"
        });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- example 1: columns not defined, all columns must be accounted for in order
        INSERT INTO customers
        VALUES (
            DEFAULT,
            'John',
            'Smith',
            '1980-10-10',
            NULL,
            '1234 Acme Road',
            'Town',
            'FL',
            DEFAULT);

        -- example 2: columns defined, can exclude auto-increment or default/null columns
        INSERT INTO customers (
            first_name,
            last_name,
            birth_date,
            address,
            city,
            state)
        VALUES (
            'John',
            'Smith',
            '1980-10-10',
            '1234 Acme Road',
            'Town',
            'FL');
        ```

## Insert Multiple Rows

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Each row of values is wrapped in its own set of parentheses, separated by commas.

    ---

    === "MongoDB"

        ```javascript
        db.shippers.insertMany([
            { name: "Shipper1" },
            { name: "Shipper2" },
            { name: "Shipper3" }
        ]);

        db.products.insertMany([
            { name: "Nintendo Switch", quantity_in_stock: 5, unit_price: 36.12 },
            { name: "iPad", quantity_in_stock: 15, unit_price: 50.00 },
            { name: "iPhone XR", quantity_in_stock: 25, unit_price: 56.72 }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        INSERT INTO shippers (name)
        VALUES ('Shipper1'),
               ('Shipper2'),
               ('Shipper3');

        INSERT INTO products (
            name,
            quantity_in_stock,
            unit_price)
        VALUES ('Nintendo Switch', 5, 36.12),
               ('iPad', 15, 50.00),
               ('iPhone XR', 25, 56.72);
        ```

## Insert Hierarchical Rows (Parent-Child Inserts)

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: The last auto-generated ID from a parent table insert can be reused when inserting related rows into a child table. The function/technique to retrieve it differs per engine.

    ---

    === "MSSQL"

        ```sql
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (2, '2021-03-05', 1);

        INSERT INTO order_items
        VALUES
            (SCOPE_IDENTITY(), 1, 1, 2.95),
            (SCOPE_IDENTITY(), 2, 1, 3.95);
        ```

    === "MongoDB"

        ```javascript
        // MongoDB generates an ObjectId automatically; insertOne returns it
        const order = db.orders.insertOne({
            customer_id: 2,
            order_date: "2021-03-05",
            status: 1
        });

        db.order_items.insertMany([
            { order_id: order.insertedId, product_id: 1, quantity: 1, unit_price: 2.95 },
            { order_id: order.insertedId, product_id: 2, quantity: 1, unit_price: 3.95 }
        ]);
        ```

    === "SQLite"

        ```sql
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (2, '2021-03-05', 1);

        INSERT INTO order_items
        VALUES
            (last_insert_rowid(), 1, 1, 2.95),
            (last_insert_rowid(), 2, 1, 3.95);
        ```

    === "MySQL"

        ```sql
        INSERT INTO orders (customer_id, order_date, status)
        VALUES (2, '2021-03-05', 1);

        INSERT INTO order_items
        VALUES
            (LAST_INSERT_ID(), 1, 1, 2.95),
            (LAST_INSERT_ID(), 2, 1, 3.95);
        ```

## Creating a Copy of a Table

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Introduces the sub-query concept — always build and test the `SELECT` statement first, then use it to create a new table from its results. MSSQL uses `SELECT ... INTO` instead of `CREATE TABLE ... AS`.

    ---

    === "MSSQL"

        ```sql
        SELECT * INTO orders_archived
        FROM orders;

        SELECT
            i.invoice_id,
            c.name,
            i.invoice_date,
            i.invoice_total,
            i.payment_total
        INTO invoices_archived
        FROM invoices i
        JOIN clients c
            ON i.client_id = c.client_id
        WHERE i.payment_date IS NOT NULL;
        ```

    === "MongoDB"

        ```javascript
        // $out writes the pipeline results to a new (or existing) collection
        db.invoices.aggregate([
            { $match: { payment_date: { $ne: null } } },
            { $out: "invoices_archived" }
        ]);
        ```

    === "SQLite / MySQL"

        ```sql
        CREATE TABLE orders_archived AS
        SELECT * FROM orders;

        CREATE TABLE invoices_archived AS
        SELECT
            i.invoice_id,
            c.name,
            i.invoice_date,
            i.invoice_total,
            i.payment_total
        FROM invoices i
        JOIN clients c
            USING (client_id)
        WHERE i.payment_date IS NOT NULL;
        ```

## Updating a Single Row

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `SET` values as literals, expressions, or other column values. `DEFAULT`/`NULL` can be used to revert a column back to its default state.

    ---

    === "MongoDB"

        ```javascript
        // update with literal values
        db.invoices.updateOne(
            { invoice_id: 1 },
            { $set: { payment_total: 10, payment_date: "2019-03-01" } }
        );

        // use an expression referencing another field (aggregation pipeline update)
        db.invoices.updateOne(
            { invoice_id: 3 },
            [{ $set: { payment_total: { $multiply: ["$invoice_total", 0.5] }, payment_date: "$due_date" } }]
        );

        // revert fields by removing them (no DEFAULT keyword)
        db.invoices.updateOne(
            { invoice_id: 1 },
            { $unset: { payment_total: "", payment_date: "" } }
        );
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- update a single row
        UPDATE invoices
        SET
            payment_total = 10,
            payment_date = '2019-03-01'
        WHERE invoice_id = 1;

        -- use an expression or another column's value
        UPDATE invoices
        SET
            payment_total = invoice_total * 0.5,
            payment_date = due_date
        WHERE invoice_id = 3;

        -- revert changes back to default values
        UPDATE invoices
        SET
            payment_total = DEFAULT,
            payment_date = NULL
        WHERE invoice_id = 1;
        ```

## Updating Multiple Rows

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: MySQL Workbench prevents updating multiple rows by default (Safe Updates). Disable it via **Edit → Preferences → SQL Editor → uncheck Safe Updates**.

    ---

    === "MongoDB"

        ```javascript
        // updateMany has no "safe mode" restriction to disable
        db.customers.updateMany(
            { birth_date: { $lt: ISODate("1990-01-01") } },
            { $inc: { points: 50 } }
        );

        db.invoices.updateMany(
            { client_id: { $in: [3, 5] } },
            [{ $set: { payment_total: { $multiply: ["$invoice_total", 0.5] }, payment_date: "$due_date" } }]
        );
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        USE sql_store;

        UPDATE customers
        SET points = points + 50
        WHERE birth_date < '1990-01-01';

        UPDATE invoices
        SET
            payment_total = invoice_total * 0.5,
            payment_date = due_date
        WHERE client_id IN (3, 5);
        ```

## Using Subqueries in Updates

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A subquery in the `WHERE` clause can resolve a value (like an ID) instead of hardcoding it. Use `IN` instead of `=` when the subquery can return multiple rows.

    ---

    === "MongoDB"

        ```javascript
        // no subquery syntax in updateMany; resolve the value(s) first, then filter
        const client = db.clients.findOne({ name: "Myworks" });
        db.invoices.updateMany(
            { client_id: client.client_id },
            [{ $set: { payment_total: { $multiply: ["$invoice_total", 0.5] }, payment_date: "$due_date" } }]
        );

        // updating multiple records: resolve a list of ids, then use $in
        const clientIds = db.clients.find({ state: { $in: ["CA", "NY"] } }).map(c => c.client_id);
        db.invoices.updateMany(
            { client_id: { $in: clientIds } },
            [{ $set: { payment_total: { $multiply: ["$invoice_total", 0.5] }, payment_date: "$due_date" } }]
        );
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        -- subquery returns the id for the given name
        UPDATE invoices
        SET
            payment_total = invoice_total * 0.5,
            payment_date = due_date
        WHERE client_id =
            (SELECT client_id
            FROM clients
            WHERE name = 'Myworks');

        -- updating multiple records: use IN instead of =
        UPDATE invoices
        SET
            payment_total = invoice_total * 0.5,
            payment_date = due_date
        WHERE client_id IN
            (SELECT client_id
            FROM clients
            WHERE state IN ('CA', 'NY'));
        ```

## Deleting Rows

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `DELETE FROM` removes rows matching the `WHERE` condition, which can also be a subquery.

    ---

    === "MongoDB"

        ```javascript
        db.invoices.deleteMany({ client_id: 1 });

        // no subquery syntax; resolve the value first, then filter
        const client = db.clients.findOne({ name: "MyWorks" });
        db.invoices.deleteMany({ client_id: client.client_id });
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        DELETE FROM invoices
        WHERE client_id = 1;

        -- with subquery
        DELETE FROM invoices
        WHERE client_id = (
            SELECT client_id
            FROM clients
            WHERE name = 'MyWorks');
        ```

## Restoring a Database

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Restore a database from its backup file. The tooling and file format differ per engine.

    ---

    === "MSSQL"

        ```sql
        RESTORE DATABASE sql_store
        FROM DISK = 'C:\backups\sql_store.bak';
        ```

    === "MongoDB"

        ```
        mongorestore --db=sql_store /path/to/dump/sql_store
        ```

    === "SQLite"

        ```
        -- restore from a .dump text file
        sqlite3 sql_store.db < sql_store.sql
        ```

    === "MySQL"

        Open the database's create/backup `.sql` file and execute it to restore the schema and data.
