# Triggers

!!! info "MySQL Syntax"
    :material-information-outline: This page uses MySQL syntax (`DELIMITER`, `SHOW TRIGGERS`, etc.). MSSQL, SQLite, and MongoDB all support triggers/change-tracking, but with substantially different syntax (e.g. MSSQL uses `inserted`/`deleted` virtual tables instead of `NEW`/`OLD` and needs no `DELIMITER`) that isn't a simple drop-in swap.

## Triggers

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Triggers execute automatically before or after an `INSERT`, `UPDATE`, or `DELETE` statement. Use `NEW` to reference the inserted/updated row, and `OLD` to reference the row before an update or delete. A trigger cannot update the same table it's attached to (would cause an infinite loop).

    ---

    ```sql
    -- example: increase payment_total when a payment is inserted
    DELIMITER $$

    CREATE TRIGGER payments_after_insert
        AFTER INSERT ON payments
        FOR EACH ROW
    BEGIN
        UPDATE invoices -- can't update the same table the trigger is on (infinite loop)
        SET payment_total = payment_total + NEW.amount
        WHERE invoice_id = NEW.invoice_id;
    END$$

    DELIMITER ;

    -- run the trigger by inserting into the payments table
    INSERT INTO payments
    VALUES (DEFAULT, 5, 3, '2021-04-18', 0.01, 1);
    ```

    ```sql
    -- example: decrease payment_total when a payment is deleted
    DELIMITER $$

    CREATE TRIGGER payments_after_delete
        AFTER DELETE ON payments
        FOR EACH ROW
    BEGIN
        UPDATE invoices
        SET payment_total = payment_total - OLD.amount
        WHERE invoice_id = OLD.invoice_id;
    END$$

    DELIMITER ;

    -- run the trigger by deleting a record from the payments table
    DELETE
    FROM payments
    WHERE payment_id = 11;
    ```

## Viewing Triggers

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `SHOW TRIGGERS` lists all triggers, optionally filtered with `LIKE`.

    ---

    ```sql
    SHOW TRIGGERS;

    -- or filter by name
    SHOW TRIGGERS LIKE 'payments%';
    ```

## Dropping Triggers

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Use `DROP TRIGGER IF EXISTS` to safely remove a trigger.

    ---

    ```sql
    DROP TRIGGER IF EXISTS payments_after_insert;
    ```

## Using Triggers for Auditing

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: A trigger can log changes to a separate audit table, capturing what changed and when.

    ---

    ```sql
    DROP TRIGGER IF EXISTS payments_after_delete;

    DELIMITER $$

    CREATE TRIGGER payments_after_delete
        AFTER DELETE ON payments
        FOR EACH ROW
    BEGIN
        UPDATE invoices
        SET payment_total = payment_total - OLD.amount
        WHERE invoice_id = OLD.invoice_id;

        -- logs the change to the audit table
        INSERT INTO payments_audit
        VALUES (OLD.client_id, OLD.date, OLD.amount, 'DELETE', NOW());
    END$$

    DELIMITER ;
    ```

## Events

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Events execute SQL code on a predetermined schedule. The MySQL event scheduler must be turned on first.

    ---

    ```sql
    -- check whether the event scheduler is on
    SHOW VARIABLES LIKE 'event%';

    -- turn it on
    SET GLOBAL event_scheduler = ON;
    ```

    ```sql
    -- example: recurring event
    DELIMITER $$

    CREATE EVENT yearly_delete_stale_audit_rows
    ON SCHEDULE
        -- for a one-time event, use AT instead, e.g. AT '2019-05-01'
        -- STARTS and ENDS are optional when using an interval
        EVERY 1 YEAR STARTS '2021-04-21' ENDS '2021-04-21'
    DO BEGIN
        DELETE FROM payments_audit
        WHERE action_date < NOW() - INTERVAL 1 YEAR;
    END$$

    DELIMITER ;
    ```

## Dropping/Viewing Events

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Events can be listed, dropped, or toggled on/off with `ALTER EVENT` instead of dropping and recreating them.

    ---

    ```sql
    -- show all events
    SHOW EVENTS;

    -- show events filtered by name
    SHOW EVENTS LIKE 'yearly%';

    -- drop an event
    DROP EVENT IF EXISTS yearly_delete_stale_audit_rows;

    -- update an event without dropping it
    ALTER EVENT yearly_delete_stale_audit_rows DISABLE; -- ENABLE / DISABLE
    ```
