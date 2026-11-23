# Exploring Schemas and Tables

## Search for Tables in a Schema

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: Query `sys.tables` and `sys.schemas` to list all tables belonging to a specific schema.

    ---

    === "MongoDB"

        No schema concept to filter by — collections live directly in a database, so listing them doesn't require a schema lookup:

        ```javascript
        db.getCollectionNames();
        ```

    === "SQLite"

        No schema/namespace concept either (SQLite databases are single-file, single-schema):

        ```sql
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
        ```

    === "MySQL"

        ```sql
        -- MySQL's "schema" is effectively the database itself
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'RTUConfigurations'
        ORDER BY table_name;
        ```

    === "MSSQL"

        ```sql
        SELECT name
        FROM sys.tables
        WHERE schema_id = (
            SELECT schema_id
            FROM sys.schemas
            WHERE name = 'RTUConfigurations'
        )
        ORDER BY name;
        ```

## Get Column Names for a Table

!!! tip "Definition"

    :material-checkbox-marked-circle-outline: See [Get column names for a specific table][get-column-names] for querying column metadata directly in SQL.

    ---

    === "MongoDB"

        No fixed columns to list — documents in a collection can each have different fields. The closest approximation is sampling documents and collecting the union of field names:

        ```javascript
        Object.keys(db.customers.findOne());
        ```

    === "SQLite"

        ```sql
        PRAGMA table_info(RTUModels);
        ```

    === "MySQL"

        ```sql
        DESCRIBE RTUModels;

        -- or
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'RTUModels';
        ```

    === "MSSQL"

        In SQL Server Management Studio, type the fully-qualified table name (e.g. `[RTUConfigurations].[RTUModels]`) in a query window and press `Alt+F1` to view the table's column and index information.

[get-column-names]: https://blog.sqlauthority.com/2017/06/29/sql-server-get-column-names-specific-table/
