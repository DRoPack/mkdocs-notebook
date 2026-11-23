# Stored Procedures

!!! info "Engine Support"
    :material-information-outline: **SQLite has no stored procedure or user-defined function support at all** \u2014 it's an embedded, single-file database with no server-side procedural engine. Where SQLite would apply, the tabs below say so explicitly. **MongoDB has no true stored procedure equivalent** either: server-side `db.system.js` scripts were deprecated in 4.2 and later removed. The closest modern options are the `$function` operator inside an aggregation pipeline (4.4+), or simply writing the logic in your application/driver code.

## Creating a Stored Procedure

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: MySQL requires temporarily changing the statement `DELIMITER` so the semicolons inside the procedure body aren't treated as the end of the statement. MSSQL uses `GO` to separate batches instead and needs no delimiter change.

    ---

    === "MSSQL"

        ```sql
        CREATE PROCEDURE get_clients
        AS
        BEGIN
            SELECT * FROM clients;
        END;
        GO

        -- calling the stored procedure
        EXEC get_clients;
        ```

    === "MongoDB"

        ```javascript
        // closest equivalent: run custom JS inside an aggregation pipeline
        db.clients.aggregate([
            { $match: {} }
        ]);
        ```

    === "SQLite"

        Not supported \u2014 SQLite has no procedural engine to store and execute server-side code.

    === "MySQL"

        ```sql
        DELIMITER $$

        CREATE PROCEDURE get_clients()
        BEGIN
            SELECT * FROM clients;
        END$$

        DELIMITER ;

        -- calling the stored procedure
        CALL get_clients();
        ```

## Creating Procedures using a GUI Tool

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Most database clients provide a GUI shortcut for creating a stored procedure, avoiding the need to type delimiters/batch separators manually.

    ---

    === "MSSQL"

        SQL Server Management Studio: right-click **Programmability \u2192 Stored Procedures \u2192 New Stored Procedure...**.

    === "MongoDB"

        Not applicable \u2014 there's no stored procedure object to create in a GUI (see the engine support note above).

    === "SQLite"

        Not applicable \u2014 no stored procedure support.

    === "MySQL"

        MySQL Workbench: right-click the **Stored Procedures** header \u2014 no need to change the delimiter manually.

## Dropping Stored Procedures

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Use `DROP PROCEDURE`, optionally with `IF EXISTS` to avoid an error when the procedure doesn't exist.

    ---

    === "MSSQL"

        ```sql
        DROP PROCEDURE get_invoices_with_balance;

        -- or, safely (SQL Server 2016+)
        DROP PROCEDURE IF EXISTS new_procedure;
        ```

    === "MongoDB"

        Not applicable \u2014 there's no persisted procedure object to drop.

    === "SQLite"

        Not applicable \u2014 no stored procedure support.

    === "MySQL"

        ```sql
        DROP PROCEDURE get_invoices_with_balance;

        -- or, safely
        DROP PROCEDURE IF EXISTS new_procedure;
        ```

## Parameters

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Parameters are declared alongside the procedure and referenced by name in the body. MSSQL parameter names are prefixed with `@`.

    ---

    === "MSSQL"

        ```sql
        DROP PROCEDURE IF EXISTS get_clients_by_state;
        GO

        CREATE PROCEDURE get_clients_by_state
            @state CHAR(2)
        AS
        BEGIN
            SELECT *
            FROM clients c
            WHERE c.state = @state;
        END;
        GO

        -- call the stored procedure with a parameter
        EXEC get_clients_by_state @state = 'CA';
        ```

    === "MongoDB"

        ```javascript
        // parameters are just function arguments in application/driver code
        function getClientsByState(state) {
            return db.clients.find({ state: state });
        }

        getClientsByState("CA");
        ```

    === "SQLite"

        Not supported \u2014 no stored procedure support.

    === "MySQL"

        ```sql
        DROP PROCEDURE IF EXISTS get_clients_by_state;

        DELIMITER $$

        CREATE PROCEDURE get_clients_by_state
        (
            state CHAR(2)
        )
        BEGIN
            SELECT *
            FROM clients c
            WHERE c.state = state;
        END$$

        DELIMITER ;

        -- call the stored procedure with a parameter
        CALL get_clients_by_state('CA');
        ```

### Exercise

=== "MSSQL"

    ```sql
    CREATE PROCEDURE get_invoices_by_client
        @clientId INT
    AS
    BEGIN
        SELECT *
        FROM invoices i
        WHERE i.client_id = @clientId;
    END;
    GO

    EXEC get_invoices_by_client @clientId = 3;
    ```

=== "MySQL"

    ```sql
    DELIMITER $$

    CREATE PROCEDURE get_invoices_by_client
    (
        clientId INT
    )
    BEGIN
        SELECT *
        FROM invoices i
        WHERE i.client_id = clientId;
    END$$

    DELIMITER ;

    CALL get_invoices_by_client(3);
    ```

## Parameters with Default Values

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: MySQL has no native default-parameter syntax, so use an `IF`/`ELSE` block (or `IFNULL`) inside the body to fall back to a default when the parameter is `NULL`. **MSSQL supports native default parameter values**, so no workaround is needed.

    ---

    === "MSSQL"

        ```sql
        -- native default value
        DROP PROCEDURE IF EXISTS get_clients_by_state;
        GO

        CREATE PROCEDURE get_clients_by_state
            @state CHAR(2) = 'CA'
        AS
        BEGIN
            SELECT *
            FROM clients c
            WHERE c.state = @state;
        END;
        GO

        EXEC get_clients_by_state; -- uses the default 'CA'
        EXEC get_clients_by_state @state = 'FL';
        ```

        ```sql
        -- return all records if the parameter is NULL, using ISNULL
        DROP PROCEDURE IF EXISTS get_clients_by_state;
        GO

        CREATE PROCEDURE get_clients_by_state
            @state CHAR(2) = NULL
        AS
        BEGIN
            SELECT *
            FROM clients c
            WHERE c.state = ISNULL(@state, c.state);
        END;
        GO

        EXEC get_clients_by_state;
        ```

    === "MongoDB"

        ```javascript
        // default parameter values are a native JavaScript feature
        function getClientsByState(state = "CA") {
            return db.clients.find({ state: state });
        }

        getClientsByState();     // uses the default 'CA'
        getClientsByState("FL");
        ```

    === "SQLite"

        Not supported \u2014 no stored procedure support.

    === "MySQL"

        ```sql
        -- set a default value when NULL is passed
        DROP PROCEDURE IF EXISTS get_clients_by_state;

        DELIMITER $$

        CREATE PROCEDURE get_clients_by_state
        (
            state CHAR(2)
        )
        BEGIN
            IF state IS NULL THEN
                SET state = 'CA';
            END IF;

            SELECT *
            FROM clients c
            WHERE c.state = state;
        END$$

        DELIMITER ;

        CALL get_clients_by_state(NULL);
        ```

        ```sql
        -- return all records if the parameter is NULL
        DROP PROCEDURE IF EXISTS get_clients_by_state;

        DELIMITER $$

        CREATE PROCEDURE get_clients_by_state
        (
            state CHAR(2)
        )
        BEGIN
            IF state IS NULL THEN
                SELECT * FROM clients;
            ELSE
                SELECT *
                FROM clients c
                WHERE c.state = state;
            END IF;
        END$$

        DELIMITER ;

        CALL get_clients_by_state(NULL);
        ```

        ```sql
        -- using IFNULL instead of an IF/ELSE block
        DROP PROCEDURE IF EXISTS get_clients_by_state;

        DELIMITER $$

        CREATE PROCEDURE get_clients_by_state
        (
            state CHAR(2)
        )
        BEGIN
            SELECT *
            FROM clients c
            WHERE c.state = IFNULL(state, c.state);
        END$$

        DELIMITER ;

        CALL get_clients_by_state(NULL);
        ```

### Exercise: Multiple Parameters

=== "MSSQL"

    ```sql
    DROP PROCEDURE IF EXISTS get_payments;
    GO

    CREATE PROCEDURE get_payments
        @client_id INT = NULL,
        @payment_method_id TINYINT = NULL
    AS
    BEGIN
        SELECT *
        FROM payments p
        WHERE p.client_id = ISNULL(@client_id, p.client_id) AND
              p.payment_method = ISNULL(@payment_method_id, p.payment_method);
    END;
    GO

    EXEC sql_invoicing.get_payments @payment_method_id = 1;
    ```

=== "MySQL"

    ```sql
    DROP PROCEDURE IF EXISTS get_payments;

    DELIMITER $$

    CREATE PROCEDURE get_payments
    (
        client_id INT,
        payment_method_id TINYINT
    )
    BEGIN
        SELECT *
        FROM payments p
        WHERE p.client_id = IFNULL(client_id, p.client_id) AND
              p.payment_method = IFNULL(payment_method_id, p.payment_method);
    END$$

    DELIMITER ;

    CALL sql_invoicing.get_payments(NULL, 1);
    ```

## Validation

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Raise a custom error and stop execution when input fails validation. MSSQL uses `THROW` (2012+) or the older `RAISERROR`; MySQL uses `SIGNAL SQLSTATE`. See [SQLSTATE common error codes](https://www.ibm.com/docs/en/db2-for-zos/11?topic=codes-sqlstate-values-common-error) for reference values.

    ---

    === "MSSQL"

        ```sql
        -- example: updates a table without validation
        CREATE PROCEDURE make_payment
            @invoice_id INT,
            @payment_amount DECIMAL(9,2),
            @payment_date DATE
        AS
        BEGIN
            UPDATE invoices
            SET
                payment_total = @payment_amount,
                payment_date = @payment_date
            WHERE invoice_id = @invoice_id;
        END;
        GO
        ```

        ```sql
        -- with validation
        CREATE PROCEDURE make_payment
            @invoice_id INT,
            @payment_amount DECIMAL(9,2),
            @payment_date DATE
        AS
        BEGIN
            IF @payment_amount <= 0
            BEGIN
                THROW 50000, 'Invalid payment amount', 1;
            END

            UPDATE invoices
            SET
                payment_total = @payment_amount,
                payment_date = @payment_date
            WHERE invoice_id = @invoice_id;
        END;
        GO

        EXEC sql_invoicing.make_payment @invoice_id = 2, @payment_amount = -100, @payment_date = '1999-01-01';
        ```

    === "MongoDB"

        ```javascript
        // validation is just a plain conditional/exception in application code
        function makePayment(invoiceId, paymentAmount, paymentDate) {
            if (paymentAmount <= 0) {
                throw new Error("Invalid payment amount");
            }

            db.invoices.updateOne(
                { invoice_id: invoiceId },
                { $set: { payment_total: paymentAmount, payment_date: paymentDate } }
            );
        }
        ```

    === "SQLite"

        Not supported \u2014 no stored procedure support.

    === "MySQL"

        ```sql
        -- example: updates a table without validation
        DELIMITER $$

        CREATE PROCEDURE make_payment (
            invoice_id INT,
            payment_amount DECIMAL(9,2),
            payment_date DATE
        )
        BEGIN
            UPDATE invoices i
            SET
                i.payment_total = payment_amount,
                i.payment_date = payment_date
            WHERE i.invoice_id = invoice_id;
        END$$

        DELIMITER ;
        ```

        ```sql
        -- with validation
        DELIMITER $$

        CREATE PROCEDURE make_payment (
            invoice_id INT,
            payment_amount DECIMAL(9,2),
            payment_date DATE
        )
        BEGIN
            IF payment_amount <= 0 THEN
                SIGNAL SQLSTATE '22003' -- error message
                    SET MESSAGE_TEXT = 'Invalid payment amount';
            END IF;

            UPDATE invoices i
            SET
                i.payment_total = payment_amount,
                i.payment_date = payment_date
            WHERE i.invoice_id = invoice_id;
        END$$

        DELIMITER ;

        CALL sql_invoicing.make_payment(2, -100, '1999-01-01');
        ```

## Output Parameters

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: MySQL uses the `OUT` keyword to declare an output parameter, with `INTO` to store a query's result into it. MSSQL uses `OUTPUT` on the parameter declaration. **Not recommended unless there's a clear use case.**

    ---

    === "MSSQL"

        ```sql
        CREATE PROCEDURE get_unpaid_invoices_for_clients
            @client_id INT,
            @invoices_count INT OUTPUT,
            @invoices_total DECIMAL(9,2) OUTPUT
        AS
        BEGIN
            SELECT
                @invoices_count = COUNT(*),
                @invoices_total = SUM(invoice_total)
            FROM invoices
            WHERE client_id = @client_id
                AND payment_total = 0;
        END;
        GO
        ```

    === "MongoDB"

        ```javascript
        // "output parameters" are just a returned object/value
        function getUnpaidInvoicesForClients(clientId) {
            const result = db.invoices.aggregate([
                { $match: { client_id: clientId, payment_total: 0 } },
                { $group: { _id: null, invoices_count: { $sum: 1 }, invoices_total: { $sum: "$invoice_total" } } }
            ]).next();
            return result;
        }
        ```

    === "SQLite"

        Not supported \u2014 no stored procedure support.

    === "MySQL"

        ```sql
        DELIMITER $$

        CREATE PROCEDURE get_unpaid_invoices_for_clients (
            client_id INT,
            OUT invoices_count INT,
            OUT invoices_total DECIMAL(9,2)
        )
        BEGIN
            SELECT
                COUNT(*),
                SUM(invoice_total)
            INTO invoices_count, invoices_total
            FROM invoices i
            WHERE i.client_id = client_id
                AND payment_total = 0;
        END$$

        DELIMITER ;
        ```

## Variables

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: MySQL session variables are prefixed with `@` and persist for the session; local variables are declared with `DECLARE` inside a procedure body. MSSQL uses `@`-prefixed local variables everywhere (there's no separate session-variable syntax) and declares them with `DECLARE ... = value` or `SET`.

    ---

    === "MSSQL"

        ```sql
        -- local variable in a batch
        DECLARE @invoices_count INT = 0;

        -- local variables inside a procedure
        CREATE PROCEDURE get_unpaid_invoices_for_clients
        AS
        BEGIN
            DECLARE @risk_factor DECIMAL(9,2) = 0;
            DECLARE @invoices_total DECIMAL(9,2);
            DECLARE @invoices_count INT;

            SELECT
                @invoices_count = COUNT(*),
                @invoices_total = SUM(invoice_total)
            FROM invoices;

            SET @risk_factor = @invoices_total / @invoices_count * 5;
            SELECT @risk_factor;
        END;
        GO
        ```

    === "MongoDB"

        ```javascript
        // just regular JavaScript variables in application/driver code
        let invoicesCount = 0;

        function getUnpaidInvoicesForClients() {
            const result = db.invoices.aggregate([
                { $group: { _id: null, invoices_count: { $sum: 1 }, invoices_total: { $sum: "$invoice_total" } } }
            ]).next();

            const riskFactor = (result.invoices_total / result.invoices_count) * 5;
            return riskFactor;
        }
        ```

    === "SQLite"

        Not supported \u2014 no stored procedure support.

    === "MySQL"

        ```sql
        -- user/session variable
        SET @invoices_count = 0;

        -- local variables
        DELIMITER $$

        CREATE PROCEDURE get_unpaid_invoices_for_clients ()
        BEGIN
            DECLARE risk_factor DECIMAL(9,2) DEFAULT 0;
            DECLARE invoices_total DECIMAL(9,2);
            DECLARE invoices_count INT;

            SELECT COUNT(*), SUM(invoice_total)
            INTO invoices_count, invoices_total -- sets the declared variables
            FROM invoices;

            SET risk_factor = invoices_total / invoices_count * 5;
            SELECT risk_factor;
        END$$

        DELIMITER ;
        ```

## Functions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: User-defined functions can only return a single value. MySQL requires declaring a characteristic such as `DETERMINISTIC`, `READS SQL DATA`, or `MODIFIES SQL DATA`; MSSQL scalar functions don't need this but must be schema-qualified (e.g. `dbo.`) when called.

    ---

    === "MSSQL"

        ```sql
        DROP FUNCTION IF EXISTS get_risk_factor_for_client;
        GO

        CREATE FUNCTION get_risk_factor_for_client (@client_id INT)
        RETURNS DECIMAL(9,2)
        AS
        BEGIN
            DECLARE @risk_factor DECIMAL(9,2) = 0;
            DECLARE @invoices_total DECIMAL(9,2);
            DECLARE @invoices_count INT;

            SELECT
                @invoices_count = COUNT(*),
                @invoices_total = SUM(invoice_total)
            FROM invoices
            WHERE client_id = @client_id;

            SET @risk_factor = @invoices_total / @invoices_count * 5;
            RETURN ISNULL(@risk_factor, 0);
        END;
        GO
        ```

    === "MongoDB"

        ```javascript
        // aggregation pipelines can run custom JS server-side via $function (4.4+)
        db.clients.aggregate([
            { $addFields: {
                risk_function: {
                    $function: {
                        body: function (clientId) {
                            const result = db.invoices.aggregate([
                                { $match: { client_id: clientId } },
                                { $group: { _id: null, count: { $sum: 1 }, total: { $sum: "$invoice_total" } } }
                            ]).next();
                            return result ? (result.total / result.count) * 5 : 0;
                        },
                        args: ["$client_id"],
                        lang: "js"
                    }
                }
            } }
        ]);
        ```

    === "SQLite"

        Not supported \u2014 no user-defined function support via SQL (custom functions can only be registered through a driver's native API, e.g. `sqlite3.create_function()` in Python).

    === "MySQL"

        ```sql
        USE `sql_invoicing`;

        DROP FUNCTION IF EXISTS `sql_invoicing`.`get_risk_factor_for_client`;

        DELIMITER $$

        USE `sql_invoicing`$$

        CREATE DEFINER=`root`@`localhost` FUNCTION `get_risk_factor_for_client`(
            client_id INT
        ) RETURNS INT
            READS SQL DATA
        BEGIN
            DECLARE risk_factor DECIMAL(9,2) DEFAULT 0;
            DECLARE invoices_total DECIMAL(9,2);
            DECLARE invoices_count INT;

            SELECT COUNT(*), SUM(invoice_total)
            INTO invoices_count, invoices_total -- sets the declared variables
            FROM invoices i
            WHERE i.client_id = client_id;

            SET risk_factor = invoices_total / invoices_count * 5;
            RETURN IFNULL(risk_factor, 0);
        END$$

        DELIMITER ;
        ```

### Calling a Function in a SELECT Statement

=== "MSSQL"

    ```sql
    SELECT
        client_id,
        name,
        dbo.get_risk_factor_for_client(client_id) AS risk_function
    FROM clients;
    ```

=== "MySQL"

    ```sql
    SELECT
        client_id,
        name,
        get_risk_factor_for_client(client_id) AS risk_function
    FROM clients;
    ```

### Dropping a Function

=== "MSSQL / MySQL"

    ```sql
    DROP FUNCTION IF EXISTS get_risk_factor_for_client;
    ```
