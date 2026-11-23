# Microsoft Graph

## HTTP with Microsoft Entra ID (Preauthorized)

Power Automate can make authenticated Microsoft Graph API calls using the **HTTP with Microsoft Entra ID (preauthorized)** connector.

This is useful when a standard Power Automate connector does not expose a Microsoft Graph property or operation that you need.

The preauthorized connector handles Microsoft Entra ID authentication on behalf of the signed-in user, eliminating the need to manually retrieve and manage an OAuth access token.

> [!NOTE]
> Make sure to use **HTTP with Microsoft Entra ID (preauthorized)** and not the similarly named **HTTP with Microsoft Entra ID** connector.

## Create the Connection

When creating the connection, use the following values.

``` powerautomate
Display name:

Microsoft Graph
```

``` powerautomate
Authentication Type:

Log in with Microsoft Entra ID
```

``` powerautomate
Base Resource URL:

https://graph.microsoft.com
```

``` powerautomate
Microsoft Entra ID Resource URI (Application ID URI):

https://graph.microsoft.com
```

Sign in using the account that should execute the Microsoft Graph requests.

## Send an HTTP Request

Add the **HTTP with Microsoft Entra ID (preauthorized)** action to the flow.

The available fields include:

- Method
- URL of the request
- Headers
- Body of the request

For example, the following Microsoft Graph endpoint retrieves the details for a Planner task:

``` powerautomate
Method:

GET
```

``` powerautomate
URL of the request:

https://graph.microsoft.com/v1.0/planner/tasks/{task-id}/details
```

A dynamic task ID can be inserted using an expression.

``` powerautomate
concat(
    'https://graph.microsoft.com/v1.0/planner/tasks/',
    outputs('Create_a_task')?['body/id'],
    '/details'
)
```

## PATCH Requests

Microsoft Graph PATCH requests can be used to update properties that might not be exposed by a standard Power Automate connector.

For example:

``` powerautomate
Method:

PATCH
```

``` powerautomate
URL of the request:

https://graph.microsoft.com/v1.0/planner/tasks/{task-id}/details
```

Some Microsoft Graph resources use ETags for concurrency control. Planner task details require the current ETag when performing an update.

``` powerautomate
Headers:

Content-Type: application/json
If-Match: <current @odata.etag>
```

The current ETag can be retrieved from the resource before performing the PATCH request.

## Building JSON Request Bodies

When inserting HTML or other dynamic strings into a JSON request body, avoid manually embedding the value inside a JSON string.

Values containing quotes or other special characters can result in invalid JSON.

Instead, Power Automate's `setProperty()` function can safely construct the JSON object.

Example:

``` powerautomate
setProperty(
    json('{}'),
    'notes',
    setProperty(
        setProperty(
            json('{}'),
            'contentType',
            'html'
        ),
        'content',
        outputs('Sanitize_HTML')
    )
)
```

This produces a JSON object similar to:

``` json
{
    "notes": {
        "contentType": "html",
        "content": "<p>Formatted HTML content</p>"
    }
}
```

Using `setProperty()` allows Power Automate to correctly handle quotes and other characters contained in the dynamic value.

## Things to Remember

- Use **HTTP with Microsoft Entra ID (preauthorized)** for authenticated Microsoft Graph requests.
- The connection operates using the permissions of the signed-in user.
- Use the standard Microsoft Graph `v1.0` API when the required functionality is available there.
- Only use Microsoft Graph `/beta` endpoints when the required property or operation is not available in `v1.0`.
- Some Graph resources require an `If-Match` header containing the current `@odata.etag` before they can be updated.
- Use `setProperty()` when constructing JSON containing dynamic HTML or other complex string values.
- Test the Graph request in **Microsoft Graph Explorer** when troubleshooting permissions, payloads, or API behavior.