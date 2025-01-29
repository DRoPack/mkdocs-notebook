# Terminal configuration

Instruction for Windows terminal setup and configuration using Oh My Posh

!!! Info

    To display all icons it is recommended to install [Nerd Font](https://www.nerdfonts.com/)

## Install Nerd Font

Install [Nerd Font](https://www.nerdfonts.com/) from the website.  Recommend using `BlexMono Nerd Font`

Install method via Drag and Drop

1. Open the Fonts folder
    - Press `Win + R` to open the run dialog
    - Type `Control Fonts` and press `Enter` to open the Fonts folder

2. Unzip the font file downloaded
3. Drag and drop
    - Drag the font file from the File Explorer into the Fonts window.
        Windows will automatically install the font
4. Update individual application settings to use the Nerd Font

## Install Oh My Posh

Install `oh-my-posh` on windows using `winget`

!!! pied-piper ""

    === "Search"

        Search for `oh-my-posh` package on `winget`. Use the package `Id` in the install command. 

        ```cmd
        C:\Users\blotter>winget search oh-my-posh

        Name       Id                      Version Match               Source
        ----------------------------------------------------------------------
        oh-my-posh XP8K0HKJFRXGCK          Unknown                     msstore
        Oh My Posh JanDeDobbeleer.OhMyPosh 24.19.0 Moniker: oh-my-posh winget
        ```

    === "Install"

        Using the `Id` from the package install `oh-my-posh`

        ```cmd
        C:\Users\blotter>winget install JanDeDobbeleer.OhMyPosh
        ```

## Install Clink

Install `Clink` on Windows using `winget`. Clink is used due to no out-of-th-box support for Windows CMD for custom prompts.

!!! pied-piper ""
    === "Search"

        Search for `Clink` package on `winget`. Use the package `Id` in the install command. 

        ```cmd
        C:\Users\blotter>winget search Clink

        Name        Id                Version  Match        Source
        ----------------------------------------------------------
        Clink       chrisant996.Clink 1.7.7                 winget
        ```

    === "Install"

        Using the `Id` from the package install `Clink`

        ```cmd
        C:\Users\blotter>winget install chrisant996.Clink
        ```

## Configure PowerShell terminal

Setup for PowerShell terminal requires a change to your `$PROFILE`

1. Locating your Profile and view file contents

!!! pied-piper ""

    === "Locate File"

        ```powershell
        C:\Users\blotter> $PROFILE

        Output:
        C:\Users\blotter\Documents\WindowsPowerShell\profile.ps1
        ```

    === "View File"

        ```powershell
        C:\Users\blotter> cat $PROFILE

        Output:
        Import-Module posh-git
        Import-Module PoShLog
        oh-my-posh init pwsh --config 'https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/kushal.omp.json' | Invoke-Expression
        ```

2. Open the file and add the following to the file

    ```txt
    // Reference local theme
    oh-my-posh init pwsh --config ~/jandedobbeleer.omp.json | Invoke-Expression

    // Reference remote theme
    oh-my-posh init pwsh --config 'https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/kushal.omp.json' | Invoke-Expression
    ```

3. Reload PowerShell Profile

    ```powershell
    C:\Users\blotter> . $PROFILE
    ```

Final configuration should look similar to this:

![PowerShell Configuration](../assets/img/terminal/OhMyPosh-PowerShell.png)

!!! tip

    Remember to update font preferences in each PowerShell applicaiton to use the Nerd Font

## Configure CMD terminal

1. Ensure [Install Clink](#install-clink) step completed

2. Create a new file called `oh-my-posh.lua` in the `Clink` program directory folder

    ```cmd title="Find Clink Directory"
    C:\Users\blotter>clink info
    ```

3. Add the following line to the `oh-my-pos.lua` file

    ```cmd title="oh-my-pos.lua"
    // Reference local theme
    load(io.popen('oh-my-posh init cmd --config C:/Users/blotter/jandedobbeleer.omp.json'):read("*a"))()

    // Reference remote theme
    load(io.popen('oh-my-posh init cmd --config "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/kushal.omp.json'):read("*a"))()
    ```

Final configuration should look similar to this:

![CMD Configuration](../assets/img/terminal/OhMyPosh-cmd.png)

!!! tip

    Remember to update font preferences in each `Windows Terminal` profile to use the Nerd Font
