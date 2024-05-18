# Custom Fences

An overview of the custom fences created for documenting HTTP calls in `Material for MkDocs`.  This feature will allow for a `Swagger` like display of API calls in markdown using code blocks with specific syntax.  

## Example

``` markdown title="Syntax"

    ``` httpCall

        Method= GET

        Path
        __blotter.sharePoint/api/GetNames/{name}

        Header
        {
            "Accept" : ""application/json;odata=nometadata""
        }

            body
        {
            "key": "value"
        }
    ```

```

**Output**

``` httpCall

    method=POST

    path
    __api/web/lists/post-example

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=nometadata"
    }

    body
    {
        "key" : "value"
    }
```

Toggle the arrow to the right of the endpoint path to display the header and body (if included)

## Usage

The first line should contain 3 backtick (`) characters followed by httpCall, then the last line should contain the same number of backticks.

```
    ```httpCall

    ```
```

Next to construct the body of the `httpCall` code block, we will be covering:

- Method
- Path
- Header
- Body

!!! Warning
    Each section of the code block requires a carriage return and indented by four spaces.

### Methods

To pick the method of the HTTP call, write `method=<method>` on the next line of the code block.  The options for `<method>` are GET, POST, PUT, PATCH, and DELETE.  If the method line is skipped, it will default to GET.  

```
    ```httpCall

       method=DELETE

    ```
```

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `GET`       | <button class="method--button method--get">GET</button>     #61affe   |
| `POST`      | <button class="method--button method--post">POST</button>    #49cc90  |
| `PUT`       | <button class="method--button method--put">PUT</button>    ##fca130 |
| `PATCH`     | <button class="method--button method--patch">PATCH</button>    #af01d9 |
| `DELETE`    | <button class="method--button method--delete">DELETE</button>    #f93e3e |

## Path

Next type`path`, then on the next line enter the api endpoint.

```
    ```httpCall

       method=DELETE

       path
       __api/web/lists/endpoint-path

    ```
```

## Header (optional)

Type `header`, then on the next line enter header information.

## Body (optional)
