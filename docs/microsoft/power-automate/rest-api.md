# SharePoint Rest APIs

## Get all List/Library

```http title="Method Get"

_api/web/lists

```

### List/Libraries

```http title="Test"

_api/web/lists

```

!!! pied-piper "Pied Piper"

## API Documentation

## GET Request Example

``` httpCall

    method=GET

    path
    __api/web/lists/get

```

## POST Request Example

``` httpCall

    method=POST

    path
    __api/web/lists/post

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=nometadata"
    }
```

## PUT Request Example

``` httpCall

    method=PUT

    path
    __api/web/lists/patch

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=verbose"
    }

    body
    {
        "key": "value"
    }
```

## Patch Request Example

``` httpCall

    method=PATCH

    path
    __api/web/lists/patch

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=verbose"
    }

    body
    {
        "key": "value"
    }
```

## Delete Request Example

``` httpCall

    method=Delete

    path
    __api/web/lists/delete

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=verbose"
    }

    body
    {
        "key": "value"
    }
```

## No Method

``` httpCall

    path
    __api/web/lists/patch

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=verbose"
    }

```
