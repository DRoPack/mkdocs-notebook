# Query Parameters

Filtering SharePoint libraries and lists via query string parameters

!!! Warning

    Refer to columns using their internal names and not the display names. Internal field names created with spaces will be encoded. Example **Order Number** will be encoded like **Order_x0020_Number**

## Single Column Filter

```html title="Syntax"
https://blotter.sharepoint.com?FilterField1=Title&FilterValue1=JIB-0111
```

```html title="Syntax for Encoded Field"
https://blotter.sharepoint.com?FilterField1=Doc_x0020__x0023_&FilterValue1=JIB-0111
```

## Multiple Column Filter

```html title="Syntax"
...sharepoint.com?FilterField1=Title&FilterValue1=JIB-0111&FilterField2=ApprovalStatus&FilterValue2=Rejected
```

## Multi-Values Filter

```html title="Syntax"
https://blotter.sharepoint.com?FilterName=Title&FilterMultiValue=JIB-0111;SOP-0212;SJP-0025
```

## Wildcard Filter

```html title="Syntax"
https://blotter.sharepoint.com?FilterName=Title&FilterMultiValue=SJP-002*
```

!!! note

    Notice the change in syntax for the Multi-Value and Wildcard filters.
