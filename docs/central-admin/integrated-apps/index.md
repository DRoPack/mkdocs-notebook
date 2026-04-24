# Integrated Apps

The **Integrated Apps** portal in the Microsoft 365 Admin Center is the recommended way to deploy Office Add-ins to users and groups within your organization.

!!! note "Publication Methods"

    Other publication methods exist besides using Integrated Apps, but they come with limitations. These include options like `sideloading`, which is primarily used for development and testing.

    [:octicons-link-external-24: Microsoft Additional publication methods](https://learn.microsoft.com/en-us/office/dev/add-ins/publish/publish)

---

## Deploy Office Add-in

1. Sign in to [:octicons-link-external-24: Microsoft 365 Admin Center](https://admin.microsoft.com)
2. From the left navigation, select **Settings** → **Integrated apps**
3. Select **Upload custom apps**
4. Complete the **Deploy New App** steps

---

!!! Example "Deploy New App"

    === "Upload Custom App"

        1. **App type**  
            - Select **Office Add-in**
        2. **Upload manifest file (.xml or .zip)**  
            - Upload your manifest file (zipped if required)
        3. Select **Next**

    === "Users"

        1. **Assign users**
            - Options:
                - Just me
                - Entire organization
                - Specific users/groups
        2. Select **Next**

    === "Deployment"

        1. **Deployment settings**
            - Review app details and assignment
            - Choose deployment method:
                - Fixed (automatically installed)
                - Available (users can install)
        2. Select **Deploy**

!!! warning

    Deployment of the add-in can take up to **72 hours** to become available to users. In practice, it typically completes within **24 hours**.

## Updating the Add-in

To update an existing add-in:

1. Go to **Settings** → **Integrated apps**
2. Select the deployed add-in
3. Choose **Update**
4. Upload the updated manifest file
5. Review assignments
6. Select **Deploy**

> Users may need to restart Outlook or refresh their browser to see updates.