# Azure App Service

Azure App Service is a fully managed platform as a service (PaaS) for building, deploying and scaling web applications. Benefits are auto scaling, security (Entra ID, Google, etc. ), Continuous deployment (CI/CD pipeline to Github for automatical deployment), built in monitoring.

> This guide walks through creating a new **Web App** in Azure App Service for hosting web applications (e.g., Outlook add-ins, APIs, internal tools).

---

## Prerequisites

- Azure subscription
- Access to the Azure Portal: :octicons-link-external-24: [Azure Portal](https://portal.azure.com/)
- Basic understanding of your app (runtime, region, etc.)

---

## Create a Resource Group (optional)

> Use a naming convention like `rg-{app}-{env}` to group all resources for a single application and environment into one manageable unit.

1. Go to **Resource groups**
2. Click **Create**
3. Enter:
   - **Name**: `rg-your-apps`
   - **Region**: same region you plan to host apps
4. Click **Review + Create**

---

## Create an App Service Plan

1. Go to **App Services**
2. Click **Create → Web App**

=== "Basics"

    - **Subscription**: select your subscription
    - **Resource Group**: select or create one
    - **Name**: enter unique name. Example: `my-company-app`
    - **Publish**: select Code or Container
    - **Runtime stack**: - Choose this based on what your app needs to execute on the **server**
        - Node (if just serving files; Express, API, etc.)
        - Other runtimes → match your backend language
    - **Operating System**: Windows (common for .NET) or Linux
    - **Region**: cloud server deployment (East US or East US 2)
    - **Pricing Plan**: B1 (Basic) → good starting point
    - **Zone Redundancy**:  Select Enabled or Disabled

=== "Database"

    - **Create a Database**:
        - Select **Yes** if your app requires a database (Azure SQL, MySQL, etc.)
        - Select **No** for:
            - Static apps (React, SPAs, Outlook add-ins)
            - Apps using external/on-prem databases
        - Can be added later if needed

=== "Deployment"

    - **Continuous deployment**:
        - Enable if deploying from GitHub/Azure DevOps
        - Automatically deploys on code changes
        - Disable if using manual deployment (ZIP, VS Code, etc.)

    - **GitHub Settings** (if enabled):
        - Select repository and branch
        - Azure will create a workflow for deployment

    - **Basic Authentication**:
        - Enable only if needed for deployment scenarios
        - Typically leave disabled unless required by your process

=== "Networking"

    - **Enable public access**:
        - Enabled → app is accessible via public URL (default, required for most apps)
        - Disabled → restricts access (used with private endpoints or internal apps)

3. Click **Review + Create**
4. Wait for validation
5. Click **Create**

Deployment takes ~30–60 seconds.

---

## Verify Deployment

After creation:

1. Go to your Web App
2. Click **Browse**
3. You should see a default Azure page

- [x] Next step: deploy the add-in via [Microsoft 365 Integrated Apps][link-integrated-apps]

[link-integrated-apps]: ../../central-admin/integrated-apps/index.md
