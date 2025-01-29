# Winget

## Using winget from command line

```cmd title="List winget packages installed"
C:\Users\blotter>winget list oh-my
```

```cmd title="Search for winget packages"
C:\Users\blotter>winget search oh-my-posh

:: Results
Name       Id                      Version Match               Source
----------------------------------------------------------------------
oh-my-posh XP8K0HKJFRXGCK          Unknown                     msstore
Oh My Posh JanDeDobbeleer.OhMyPosh 24.19.0 Moniker: oh-my-posh winget
```

```cmd title="Install winget package"
:: Grab the ID from the output of search
C:\Users\blotter>winget install JanDeDobbeleer.OhMyPosh
```

```cmd title="Upgrade winget package"
:: Grab the ID from the output of search
C:\Users\blotter>winget upgrade JanDeDobbeleer.OhMyPosh
```
