# SharePoint Rest APIs

## Get List Items

There are two options to get list/library items, either the `GetByTitle` and `guid` endpoint.  The preferred way is to use the `guid` method.  Using the `GetByTitle` method could break if the list/library name gets changed.

### Get By Title

``` httpCall

    method=GET

    path
    _api/Web/Lists/GetByTitle('blotterLibrary')

    header
    {
    "content-type": "application/json;odata=verbose",
    "accept": "application/json;odata=verbose"
    }
```

### Get By Guid

``` httpCall

    method=GET

    path
    _api/Web/Lists(guid'84e5321e-c28d-4d8d-8a4a-5f377ad4bcf0')

    header
    {
    "content-type": "application/json;odata=nometadata",
    "accept": "application/json;odata=nometadata"
    }
```

!!! info
    Notice for both calls, a different header is used. Verbose will return more information which maybe be useful when first building the endpoint.  Nometadata will return minimal (specific) information requested.

## Update Properites

This example updates the metadata properties of a list/library item

``` httpCall

    method=PATCH

    path
    _api/Web/Lists(guid'84e5321e-c28d-4d8d-8a4a-5f377ad4bcf0')/items({ID})

    header
    {
    "content-type": "application/json;odata=verbose",
    "IF-MATCH": "*",
    "X-HTTP-Method": "PATCH"
    }

    body
    {
    "__metadata":
        {
        "type":"SP.Data.BlotterLibraryItem"
        },
        "Document_x0020_Type" :  "DropDownItem",
        "Meeting_x0020_Date" : "2024-05-04",
        "Title" : "myFileName",
        "FileLeafRef" : "myFileName.docx"
    }
```

!!! warning

    In the body of the request for type, ensure the first letter of the list/library name is capitalized.  Example: Internal list name is blotterLibrary.  It must be BlotterLibrary in the request body.

## Move Files

This example moves file to a new folder within the same library

```httpCall

    method=POST

    path
    _api/SP.MoveCopyUtil.MoveFileByPath(overwrite=@a1)?@a1=true

    header
    {
    "content-type": "application/json;odata=verbose",
    "accept": "application/json;odata=verbose"
    }

    body
    {
        "srcPath": {
            "__metadata": {
                "type": "SP.ResourcePath"
            },
            "DecodedUrl": "https://blotter.sharepoint.com/blotterLibrary/FileName.docx"
        },
        "destPath": {
            "__metadata": {
                "type": "SP.ResourcePath"
            },
            "DecodedUrl": "https://blotter.sharepoint.com/blotterLibrary/NewFolder/FileName.docx"
        }
    }
```

## Create Folder

This example creates a new folder in a library

```httpCall

    method=POST

    path
    _api/web/folders

    header
    {
    "content-type": "application/json;odata=verbose",
    "accept": "application/json;odata=verbose"
    }

    body
    {
    "__metadata": {
        "type": "SP.Folder"
    },
    "ServerRelativeUrl": "blotterLibrary/NewFolder"
    }
```
