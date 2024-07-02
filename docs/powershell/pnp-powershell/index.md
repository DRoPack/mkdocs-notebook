# PnP PowerShell Main

## Check Modules Installed

```powershell
    get-modules
    get-modules SharePointPnpPowerShell2019 | Select Version
```

## Check Available Cmdlet

```powershell
    get-command -Module SharePointPnpPowerShell2019
```

## Connect to SharePoint

```powershell
    $web = "https://blotter.sharepoint.com"
    Connect-PnPOnline $web -CurrentCredentials
```
