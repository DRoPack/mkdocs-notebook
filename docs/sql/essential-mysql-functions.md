# Essential MySQL Functions

## Numeric Functions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Common functions for rounding, truncating, and manipulating numeric values.

    ---

    ```sql
    SELECT ROUND(5.73);        -- 6
    SELECT ROUND(5.73, 1);     -- 5.7, optional argument sets precision
    SELECT TRUNCATE(5.7345, 2);-- 5.73, drops digits beyond the argument (no rounding)
    SELECT CEILING(5.2);       -- 6, smallest integer greater than or equal to the number
    SELECT FLOOR(5.2);         -- 5, largest integer less than or equal to the number (no rounding)
    SELECT ABS(-5.2);          -- 5.2, always returns a positive value
    SELECT RAND();             -- random number between 0 and 1
    ```

## String Functions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Common functions for inspecting, trimming, extracting, and combining string values.

    ---

    ```sql
    SELECT LENGTH('Sky');
    SELECT UPPER('Sky');
    SELECT LOWER('Sky');
    SELECT LTRIM('Sky');            -- left trim
    SELECT RTRIM('Sky');            -- right trim
    SELECT TRIM('Sky');             -- trims leading and trailing spaces
    SELECT LEFT('Sky', 2);          -- 2 characters from the left
    SELECT RIGHT('Sky', 2);         -- 2 characters from the right
    SELECT SUBSTRING('Sky', 2, 1);  -- 1 character starting at position 2
    SELECT LOCATE('k', 'Sky');      -- position of 'k'
    SELECT REPLACE('Sky', 'y', 'ies');
    SELECT CONCAT('first', 'last');

    SELECT CONCAT(first_name, ' ', last_name) AS full_name
    FROM customers;
    ```

## Date Functions

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Functions for retrieving the current date/time and extracting date parts. Using functions like `YEAR(NOW())` keeps filters dynamic instead of hardcoding a value.

    ---

    ```sql
    SELECT NOW(),
           CURDATE(),
           CURTIME(),
           YEAR(NOW()),
           MONTH(NOW()),
           MONTHNAME(NOW()),
           DAY(NOW()),
           DAYNAME(NOW()),
           HOUR(NOW()),
           MINUTE(NOW());

    SELECT EXTRACT(YEAR FROM NOW());

    -- check for orders in the current year (dynamic, not hardcoded)
    SELECT *
    FROM orders
    WHERE YEAR(order_date) >= YEAR(NOW());
    ```

## Formatting Dates and Times

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `DATE_FORMAT()` and `TIME_FORMAT()` render dates/times using format specifiers.

    ---

    ```sql
    SELECT DATE_FORMAT(NOW(), '%M %d %Y'),
           TIME_FORMAT(NOW(), '%H:%i %p');
    ```

## Calculating Dates and Times

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `DATE_ADD`/`DATE_SUB` shift a date by an interval. `DATEDIFF` returns the difference in days. `TIME_TO_SEC` converts a time to elapsed seconds since midnight, useful for computing the difference between two times.

    ---

    ```sql
    SELECT DATE_ADD(NOW(), INTERVAL 1 HOUR),
           DATE_ADD(NOW(), INTERVAL 1 YEAR),
           DATE_ADD(NOW(), INTERVAL -1 HOUR), -- subtract 1 hour
           DATE_SUB(NOW(), INTERVAL 1 HOUR);  -- subtract 1 hour

    SELECT DATEDIFF('2019-01-05 17:00', '2019-01-01');

    SELECT TIME_TO_SEC('09:00'); -- time elapsed from midnight, in seconds

    SELECT TIME_TO_SEC('9:02') - TIME_TO_SEC('9:00'); -- elapsed time between two times
    ```

## IFNULL and COALESCE

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `IFNULL(value, fallback)` returns a fallback when a value is `NULL`. `COALESCE` accepts multiple arguments and returns the first non-`NULL` value.

    ---

    ```sql
    SELECT
        order_id,
        IFNULL(shipper_id, 'N/A') AS Shipper
    FROM orders;

    SELECT
        order_id,
        COALESCE(shipper_id, comments, 'N/A') AS Shipper
    FROM orders;
    ```

### Exercise

```sql
SELECT
    CONCAT(first_name, ' ', last_name) AS customer,
    IFNULL(phone, 'Unknown') AS phone
FROM customers;
```

## IF Function

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `IF(condition, value_if_true, value_if_false)` returns one of two values based on a condition.

    ---

    ```sql
    SELECT
        order_id,
        order_date,
        IF(YEAR(order_date) = YEAR('2019-01-01'), 'Active', 'Archived') AS status
    FROM orders;

    SELECT
        p.product_id,
        p.name,
        COUNT(*) AS orders,
        IF(COUNT(*) > 1, 'Many times', 'Once') AS frequency
    FROM products p
    JOIN order_items USING (product_id)
    GROUP BY product_id, name;
    ```

## CASE Operator

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: `CASE` evaluates a list of `WHEN` conditions in order and returns the matching `THEN` value, falling back to `ELSE` if none match.

    ---

    ```sql
    SELECT
        order_id,
        CASE
            WHEN YEAR(order_date) = YEAR(NOW()) THEN 'Active'
            WHEN YEAR(order_date) = YEAR(NOW()) - 1 THEN 'Last Year'
            WHEN YEAR(order_date) < YEAR(NOW()) - 1 THEN 'Archived'
            ELSE 'Future'
        END AS category
    FROM orders;
    ```

### Exercise

```sql
SELECT
    CONCAT(first_name, ' ', last_name) AS customers,
    points,
    CASE
        WHEN points > 3000 THEN 'Gold'
        WHEN points >= 2000 THEN 'Silver'
        ELSE 'Bronze'
    END AS category
FROM customers;
```
