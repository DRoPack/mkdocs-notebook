# Update Versionsing and Publishing

When preparing an SPFx update for SharePoint 2019, version control and packaging must be precise.
Follow these steps to ensure the deployment is recognized and successful.

## 1. `package-solution.json`

**File:** `config/package-solution.json`

Update the version **each time** you deploy a new package:

```json
"solution": {
  "name": "your-solution",
  "id": "same-guid-as-before",
  "version": "1.0.0.3"  // ⬅️ increment this
}
```

📌 Why SPFx uses 4 parts here: SharePoint's app catalog tracks changes at a more granular level. 
The 4th number (REVISION) helps trigger updates even when the major/minor/patch stay the same.

---

## 2. `package.json`

**File:** `package.json`  
(optional but recommended for internal tracking)

```json
"version": "1.0.3"
```

Format: MAJOR.MINOR.PATCH
Used by Node.js/npm for packages. Example:

1.0.0 – Initial release

1.1.0 – Adds new features, backward compatible

1.1.1 – Fixes bugs, backward compatible

---

## 3. `WebPart.manifest.json` (optional, if UI changed)

**Update if you're changing titles, descriptions, icons, or categories.**

```json
"title": { "default": "New Display Name" },
"description": { "default": "Updated description" }
```

---

## 4. Rebuild and Repackage

Always clean and repackage before uploading:

```bash
gulp clean
gulp build --ship
gulp bundle --ship
gulp package-solution --ship
```


## 5. Upload `.sppkg` to the App Catalog

1. Navigate to your SharePoint 2019 **App Catalog** site (typically at `/sites/apps`).
2. Open the **Apps for SharePoint** document library.
3. Upload your updated `.sppkg` file found in the `sharepoint/solution/` folder.
4. When prompted, confirm replacing the existing version.
5. Wait for the upload to finish—there will be **no tenant-wide deployment prompt** in SP2019.

---

## 6. Add App to Sites (if needed)

1. Go to your target site collection.
2. Choose **Site Contents > Add an App**.
3. Select your updated app and add it.
4. This will activate the feature on the site.

---

## 7. Validate the Deployment

- Check that your updated web part renders correctly.
- Use F12 developer tools to confirm scripts and assets are loading without 404s.
- Refresh browser cache if necessary.
