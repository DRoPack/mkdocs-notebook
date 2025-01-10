# Creating an SPFx Project

## Create Project

Open `cmd` command prompt and navigate to the folder where the project will be stored

```cmd title="Navigating Folders"
C:\Users\Me> cd repos\spfx-project
```

```cmd title="Create Project Directory"
C:\Users\Me\repos\spfx-project> mkdir HelloWorld
```

```cmd title="Navigate to new Project Directory"
C:\Users\Me\repos\spfx-project\HelloWord> mkdir HelloWorld
```

```cmd title="Run Yeoman Generator"
C:\Users\Me\repos\spfx-project\HelloWord> yo @microsoft/sharepoint


     _-----_
    |       |    .--------------------------.
    |--(o)--|    |      Welcome to the      |
   `---------´   |  SharePoint Client-side  |
    ( _´U`_ )    |    Solution Generator    |
    /___A___\    '--------------------------'
     |  ~  |
   __'.___.'__
 ´   `  |° ´ Y `

Let's create a new SharePoint solution.
? What is your solution name? hello-world
```

!!! info
    By default the `Yeoman` generator will do an `npm install` and install all the dependencies if you wish to skip the `npm install` portion.  Run the follow flag.

    ```cmd title="Skip NPM Install"
    yo @microsoft/sharepoint --skip-install
    ```
    
    After the project is created, it's the developers responsibility to run the `npm install`.  The benefit of doing it this way is that the generator will create the scaffold out the project faster.

## Yeoman Generator Prompts

!!! note
    The `Yeoman` prompts for SharePoint will vary depending on the version of `Yeoman` install.

## Install Local Certificate

This command just needs run once on the development machine.  It is not local to the project folder. This allows `Gulp` to serve the project up in the hosted workbench with a trusted certificate.

```cmd title="Install Dev Certificate"
gulp trust-dev-cert
```

!!! warn
    It may prompt you for credentials to install the dev certificate

## Update Workbench

Microsoft has deprecated the local workbench starting with `SPFx v1.13` and only supports the hosted workbench served from a SharePoint site.  Append <_layouts/15/workbench.aspx> to the url where you will be testing the `SPFx` solution.

Inside your project navigate to the config folder, then server.json file.  Then update the `initialPage` property inside the file with "<https://blotter.sharepoint/_layouts/workbench.aspx>".
