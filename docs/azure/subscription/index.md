# Azure Subscription

Azure subscriptions are used for **billing** and **governance**.

- Provide billing separation to track costs per subscription
- Allow organizations to monitor spending across teams, projects, or environments
- Support access control (RBAC) by assigning permissions at the subscription level for better isolation

Creating multiple subscriptions provides clear separation of environments. For example:

- Development
- Testing
- Production

---

- [Azure Portal](https://portal.azure.com/)

## Create Subscription

!!! note "Permissions"
To create subscriptions under a Microsoft Customer Agreement (MCA), you must have one of the following:

    - Owner or Contributor role on:
        - Invoice section
        - Billing profile
        - Billing account
    - **OR** the Azure subscription creator role

### Steps

1. Navigate to **Subscriptions**
2. Select **+ Add**

3. On the _Create a subscription_ page:
   - Enter **Subscription name**  
     _Example: `My-Apps-Prod`_
   - Select **Billing account**
   - Select **Billing profile**
   - Select **Invoice section**
   - Select **Plan** (e.g., Microsoft Azure Plan)

4. Select **Next** to review the remaining configuration tabs
5. Select **Review + create**, then **Create**
