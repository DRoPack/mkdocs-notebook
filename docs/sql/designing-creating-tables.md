# Designing and Creating Tables

## Creating a Database

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `CREATE DATABASE` creates a new database, and `USE` switches the active database for subsequent statements.

    ---

    === "MongoDB"

        No explicit create step — a database (and any collection referenced) is created automatically the first time data is written to it:

        ```javascript
        use sql_store;

        db.customers.insertOne({ first_name: "John" }); // creates the db + collection
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        CREATE DATABASE sql_store;

        USE sql_store;
        ```

## Common Data Types

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Choose the smallest data type that reliably fits the data — this keeps storage and indexes efficient. The exact type names differ per engine.

    ---

    === "MSSQL"

        | Category | Examples | Notes |
        |----------|----------|-------|
        | Integer | `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | Same ranges as MySQL |
        | Decimal | `DECIMAL(9,2)`, `FLOAT`, `REAL` | Use `DECIMAL` for money |
        | String | `CHAR(n)`, `VARCHAR(n)`, `NVARCHAR(n)` | `NVARCHAR` for Unicode text |
        | Date/Time | `DATE`, `DATETIME2`, `TIME` | `DATETIME2` replaces the legacy `DATETIME` |
        | Boolean | `BIT` | `0`/`1`, no native `BOOLEAN` type |
        | Binary | `VARBINARY`, `IMAGE` | `IMAGE` is deprecated in favor of `VARBINARY(MAX)` |

    === "MongoDB"

        No fixed schema — fields are typed per-document using BSON types:

        | Category | BSON Type | Notes |
        |----------|-----------|-------|
        | Integer | `int`, `long` | 32-bit and 64-bit integers |
        | Decimal | `double`, `decimal128` | `decimal128` for exact precision (money) |
        | String | `string` | UTF-8, no fixed-length variant |
        | Date/Time | `date` | Stored as UTC milliseconds since epoch |
        | Boolean | `bool` | Native boolean type |
        | Binary | `binData` | For binary data such as files or images |

    === "SQLite"

        SQLite uses dynamic typing with only 5 storage classes — declared types like `VARCHAR(50)` are accepted but not enforced:

        | Category | Storage Class | Notes |
        |----------|----------|-------|
        | Integer | `INTEGER` | Variable-width, up to 64-bit |
        | Decimal | `REAL` | 8-byte floating point; no native fixed-precision decimal |
        | String | `TEXT` | No separate fixed-length type |
        | Date/Time | `TEXT`, `INTEGER`, or `REAL` | No dedicated date/time storage class — store as ISO8601 text or Unix time |
        | Boolean | `INTEGER` | `0`/`1`, no native `BOOLEAN` type |
        | Binary | `BLOB` | Stored exactly as input |

    === "MySQL"

        | Category | Examples | Notes |
        |----------|----------|-------|
        | Integer | `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | `TINYINT` for small ranges (e.g. status flags), `INT`/`BIGINT` for IDs |
        | Decimal | `DECIMAL(9,2)`, `FLOAT`, `DOUBLE` | Use `DECIMAL` for money — exact precision, no rounding errors |
        | String | `CHAR(n)`, `VARCHAR(n)`, `TEXT` | `VARCHAR` for variable-length text, `CHAR` for fixed-length codes |
        | Date/Time | `DATE`, `DATETIME`, `TIMESTAMP`, `TIME` | `TIMESTAMP` is timezone-aware and range-limited (up to 2038) |
        | Boolean | `TINYINT(1)`, `BOOLEAN` | MySQL stores `BOOLEAN` as `TINYINT(1)` under the hood |
        | Binary | `BLOB`, `VARBINARY` | For binary data such as files or images |

## Creating a Table

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `CREATE TABLE` defines the table's columns, data types, and constraints. `PRIMARY KEY` uniquely identifies each row, and `AUTO_INCREMENT`/`IDENTITY` generates sequential values automatically.

    ---

    === "MSSQL"

        ```sql
        CREATE TABLE customers (
            customer_id INT IDENTITY(1,1) PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            points INT NOT NULL DEFAULT 0,
            email VARCHAR(255) NOT NULL UNIQUE
        );
        ```

    === "MongoDB"

        ```javascript
        // MongoDB is schemaless by default; a collection is the rough
        // equivalent of a table, created implicitly on first insert or
        // explicitly with an optional JSON schema validator
        db.createCollection("customers", {
            validator: {
                $jsonSchema: {
                    bsonType: "object",
                    required: ["first_name", "last_name", "email"],
                    properties: {
                        first_name: { bsonType: "string" },
                        last_name: { bsonType: "string" },
                        points: { bsonType: "int" },
                        email: { bsonType: "string" }
                    }
                }
            }
        });
        ```

    === "SQLite"

        ```sql
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            points INTEGER NOT NULL DEFAULT 0,
            email VARCHAR(255) NOT NULL UNIQUE
        );
        ```

    === "MySQL"

        ```sql
        CREATE TABLE customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            points INT NOT NULL DEFAULT 0,
            email VARCHAR(255) NOT NULL UNIQUE
        );
        ```

## Foreign Keys and Constraints

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A `FOREIGN KEY` enforces referential integrity by linking a column to a primary key in another table. `ON DELETE`/`ON UPDATE` define what happens to child rows when the referenced row changes.

    ---

    === "MongoDB"

        No enforced foreign keys:

        - MongoDB has no native referential-integrity constraint between collections
        - The convention is to store a reference field (e.g. `customer_id`) and either enforce/cascade the relationship in application code, or validate it with `$lookup` at query time
        - `ON DELETE`/`ON UPDATE` cascading behavior must also be implemented manually (e.g. in a driver-level hook or a change stream listener)

    === "MSSQL / SQLite / MySQL"

        ```sql
        CREATE TABLE orders (
            order_id INT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            order_date DATE NOT NULL,
            status TINYINT NOT NULL DEFAULT 1,
            FOREIGN KEY fk_orders_customers (customer_id)
                REFERENCES customers (customer_id)
                ON UPDATE CASCADE
                ON DELETE NO ACTION
        );
        ```

        - `CASCADE` — apply the same change (update/delete) to child rows
        - `NO ACTION`/`RESTRICT` — block the change if child rows reference it
        - `SET NULL` — set the foreign key column to `NULL` in child rows

## Altering a Table

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `ALTER TABLE` adds, modifies, or drops columns and constraints on an existing table without recreating it. Modifying an existing column's type/constraints uses different syntax per engine, and MongoDB has no schema to alter.

    ---

    ```sql
    -- add a column (same syntax across MySQL, MSSQL, SQLite)
    ALTER TABLE customers
    ADD phone VARCHAR(15) NULL;

    -- drop a column (same syntax across MySQL, MSSQL, SQLite 3.35+)
    ALTER TABLE customers
    DROP COLUMN phone;

    -- add a foreign key to an existing table
    ALTER TABLE orders
    ADD FOREIGN KEY fk_orders_customers (customer_id)
        REFERENCES customers (customer_id);
    ```

    === "MSSQL"

        ```sql
        -- modify a column's type/constraints
        ALTER TABLE customers
        ALTER COLUMN phone VARCHAR(20) NOT NULL;
        ```

    === "MongoDB"

        ```javascript
        // no schema to alter; update the validator instead
        db.runCommand({
            collMod: "customers",
            validator: { $jsonSchema: { /* updated schema */ } }
        });
        ```

    === "SQLite"

        ```sql
        -- SQLite cannot modify a column's type/constraints directly;
        -- create a new table, copy the data, then drop/rename
        ```

    === "MySQL"

        ```sql
        -- modify a column's type/constraints
        ALTER TABLE customers
        MODIFY phone VARCHAR(20) NOT NULL DEFAULT '';
        ```

## Dropping Tables and Databases

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `DROP TABLE`/`DROP DATABASE` permanently delete the object and all its data. Use `IF EXISTS` to avoid an error if it doesn't exist.

    ---

    === "MongoDB"

        ```javascript
        db.customers.drop();

        db.dropDatabase(); // drops whichever database is currently selected
        ```

    === "MSSQL / SQLite / MySQL"

        ```sql
        DROP TABLE IF EXISTS customers;

        DROP DATABASE IF EXISTS sql_store;
        ```

## Indexes

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: An index speeds up lookups and sorting on the indexed column(s) at the cost of extra storage and slower writes. Primary keys and unique constraints are indexed automatically. Creating an index uses the same `CREATE INDEX` syntax across MySQL, MSSQL, and SQLite, but viewing and dropping indexes differ per engine.

    ---

    ```sql
    -- create an index (same syntax across MySQL, MSSQL, SQLite)
    CREATE INDEX idx_customers_state ON customers (state);

    -- composite index on multiple columns
    CREATE INDEX idx_customers_state_points ON customers (state, points);
    ```

    === "MSSQL"

        ```sql
        -- view indexes for a table
        EXEC sp_helpindex 'customers';

        -- drop an index
        DROP INDEX idx_customers_state ON customers;
        ```

    === "MongoDB"

        ```javascript
        // view indexes for a collection
        db.customers.getIndexes();

        // create an index
        db.customers.createIndex({ state: 1 });

        // drop an index
        db.customers.dropIndex("state_1");
        ```

    === "SQLite"

        ```sql
        -- view indexes for a table
        PRAGMA index_list(customers);

        -- drop an index (no ON clause; index names are global)
        DROP INDEX idx_customers_state;
        ```

    === "MySQL"

        ```sql
        -- view indexes for a table
        SHOW INDEXES IN customers;

        -- drop an index
        DROP INDEX idx_customers_state ON customers;
        ```

## Transactions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A transaction groups multiple statements so they either all succeed (`COMMIT`) or all roll back (`ROLLBACK`) together, keeping the database consistent. The keyword to begin a transaction differs slightly per engine, and MongoDB transactions require a session and a replica set.

    ---

    === "MSSQL"

        ```sql
        BEGIN TRANSACTION;

        UPDATE invoices
        SET payment_total = payment_total + 10
        WHERE invoice_id = 1;

        UPDATE accounts
        SET balance = balance - 10
        WHERE account_id = 1;

        COMMIT;
        -- or ROLLBACK; to undo both statements if something went wrong
        ```

    === "MongoDB"

        ```javascript
        const session = client.startSession();
        session.startTransaction();
        try {
            db.invoices.updateOne(
                { invoice_id: 1 },
                { $inc: { payment_total: 10 } },
                { session }
            );
            db.accounts.updateOne(
                { account_id: 1 },
                { $inc: { balance: -10 } },
                { session }
            );
            session.commitTransaction();
        } catch (error) {
            session.abortTransaction();
        }
        ```

    === "SQLite"

        ```sql
        BEGIN TRANSACTION;

        UPDATE invoices
        SET payment_total = payment_total + 10
        WHERE invoice_id = 1;

        UPDATE accounts
        SET balance = balance - 10
        WHERE account_id = 1;

        COMMIT;
        -- or ROLLBACK; to undo both statements if something went wrong
        ```

    === "MySQL"

        ```sql
        START TRANSACTION;

        UPDATE invoices
        SET payment_total = payment_total + 10
        WHERE invoice_id = 1;

        UPDATE accounts
        SET balance = balance - 10
        WHERE account_id = 1;

        COMMIT;
        -- or ROLLBACK; to undo both statements if something went wrong
        ```
