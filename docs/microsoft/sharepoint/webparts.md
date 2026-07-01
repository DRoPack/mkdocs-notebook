# Web Parts

!!! note

    Source files should be uploaded to the **Resources** library at the root of each site collection.

    Example: `https://blotter.sharepoint.com/resources/scripts/myfile.css`

    Centralizing JavaScript, CSS, ASPX pages, and other reusable assets in a single library simplifies maintenance and deployment. A single file can be referenced by multiple pages, web parts, lists, and subsites without duplicating content.


## Script Editor Web Part

```html title="JavaScript References"
<script
  type="text/javascript"
  src="/resources/scripts/FieldServiceCalendar.js"
></script>
```

```html title="CSS References"
<link
  rel="stylesheet"
  type="text/css"
  href="/resources/scripts/hideEditFormRibbon.css"
/>
```
