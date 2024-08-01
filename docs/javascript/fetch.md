# Fetch API

Basic JavaScript fetch used with SharePoint Rest API

```js
// Call SharePoint API (async)
async function fetchSharePointData(itemId) {
  const baseUrl = _spPageContextInfo.webAbsoluteUrl;
  const listGuid = "33FB77C9-C3DB-4A40-8DC7-165B2A78EE0B"; // Compliance Documents
  const baseAPI = `${baseUrl}/_api/web/lists(guid'${listGuid}')`;
  const select = `$select=Id,Title,Doc_x0020__x0023_,docNumber,spPerson/Title,spLookup/ID`;
  const expand = `$expand=spPerson,spLookup`;

  // SharePoint API Headers
  const payload = {
    method: "GET",
    headers: { Accept: "application/json; odata=nometadata" },  // odata=verbose
    credentials: "same-origin", // or credentials: 'include'
  };

  try {
    const response = await fetch(
      `${baseAPI}/items(${itemId})?${select}&${expand}`,
      payload
    );

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    const data = await response.json();
    console.log(data);  // if accept header is verbose, use data.value

  } catch (error) {
    console.error("Fetch Error:", error);
    throw error; // Re-throw to handle it in the event listener if needed
  }
}

fetchSharePointData(itemId);
```
