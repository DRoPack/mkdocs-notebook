# Views

## Creating Views

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A view is a saved query that can be queried like a table. `CREATE VIEW` stores the query definition, not the data itself.

    ---

    === "MongoDB"

        ```javascript
        // a MongoDB "view" is a saved, read-only aggregation pipeline
        db.createView("clients_balance", "clients", [
            { $lookup: { from: "invoices", localField: "client_id", foreignField: "client_id", as: "invoices" } },
            { $addFields: {
                balance: { $sum: {
                    $map: { input: "$invoices", as: "i", in: { $subtract: ["$$i.invoice_total", "$$i.payment_total"] } }
                } }
            } },
            { $project: { invoices: 0 } }
        ]);
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        CREATE VIEW clients_balance AS
        SELECT
            c.client_id,
            c.name,
            SUM(i.invoice_total - i.payment_total) AS balance
        FROM clients c
        JOIN invoices i USING (client_id)
        GROUP BY client_id, name;
        ```

## Altering and Dropping Views

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Use `DROP VIEW` to remove a view. Updating a view's definition in place (without dropping it first) uses different syntax per engine — SQLite has no update-in-place syntax at all. Save the view's query locally after creation so it can be edited later — if it wasn't saved, click the wrench icon while hovering over the view in the client.

    ---

    ```sql
    -- drop a view (same syntax across MySQL, MSSQL, SQLite)
    DROP VIEW clients_balance;
    ```

    === "MSSQL"

        ```sql
        -- update a view (2016+)
        CREATE OR ALTER VIEW clients_balance AS
        -- ... updated SELECT statement
        ```

    === "MongoDB"

        ```javascript
        // a "view" in MongoDB is a read-only aggregation pipeline over a collection
        db.createView("clients_balance", "clients", [
            { $lookup: { from: "invoices", localField: "client_id", foreignField: "client_id", as: "invoices" } }
        ]);
        ```

    === "SQLite"

        ```sql
        -- no update-in-place syntax; drop and recreate
        DROP VIEW IF EXISTS clients_balance;

        CREATE VIEW clients_balance AS
        -- ... updated SELECT statement
        ```

    === "MySQL"

        ```sql
        -- update a view
        CREATE OR REPLACE VIEW clients_balance AS
        -- ... updated SELECT statement
        ```

## Updatable Views

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A view is updatable (supports `INSERT`, `UPDATE`, `DELETE`) as long as it does **not** use `DISTINCT`, aggregate functions (`MIN`, `MAX`, `SUM`, etc.), `GROUP BY`/`HAVING`, or `UNION`. Modifying data through an updatable view modifies the underlying table.

    ---

    === "MongoDB"

        Not applicable — views created with `createView` are always read-only; there's no updatable-view concept to opt into.

    === "SQLite"

        Views are **read-only by default**, regardless of how simple the query is. To support `INSERT`/`UPDATE`/`DELETE` through a view, you must manually define `INSTEAD OF` triggers that translate those operations onto the base table(s).

    === "MSSQL / MySQL"

        ```sql
        CREATE OR REPLACE VIEW invoices_with_balance AS
        SELECT
            invoice_id,
            number,
            client_id,
            invoice_total,
            payment_total,
            invoice_total - payment_total AS balance,
            invoice_date,
            due_date,
            payment_date
        FROM invoices
        WHERE (invoice_total - payment_total) > 0;

        -- deleting from the view deletes the record from the underlying table as well
        DELETE FROM invoices_with_balance
        WHERE invoice_id = 1;

        -- updating the view updates the underlying table
        UPDATE invoices_with_balance
        SET due_date = DATE_ADD(due_date, INTERVAL 2 DAY)
        WHERE invoice_id = 2;
        ```

## WITH CHECK OPTION Clause

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `WITH CHECK OPTION` prevents updates through a view that would cause the affected row to no longer satisfy the view's `WHERE` condition (i.e. it would disappear from the view).

    ---

    === "MongoDB"

        Not applicable — MongoDB views are read-only, so there's no update path to constrain.

    === "SQLite"

        **Not supported** — SQLite has no `WITH CHECK OPTION` clause at all (views are read-only regardless, see [Updatable Views](#updatable-views)).

    === "MSSQL / MySQL"

        ```sql
        CREATE OR REPLACE VIEW invoices_with_balance AS
        SELECT
            invoice_id,
            number,
            client_id,
            invoice_total,
            payment_total,
            invoice_total - payment_total AS balance,
            invoice_date,
            due_date,
            payment_date
        FROM invoices
        WHERE (invoice_total - payment_total) > 0
        WITH CHECK OPTION;
        ```

## Benefits of Views

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Views simplify future changes to the underlying tables (queries against the view keep working) and can restrict access to specific columns or rows of data.
