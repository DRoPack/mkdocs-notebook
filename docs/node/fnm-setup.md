# FNM Setup for Windows (CMD + PowerShell + Clink + Oh My Posh)

This guide covers how to install [Fast Node Manager (FNM)](https://github.com/Schniz/fnm) and configure it for use with:

- **CMD (Command Prompt)**
- **PowerShell**
- **Clink**
- **Oh My Posh**

---

## Why FNM?

FNM is a faster, cross-platform alternative to NVM:

- Written in Rust
- Native Windows support
- Faster version switching and installs
- Automatically loads versions from `.nvmrc` or `.node-version`

---

## Prerequisites

- Windows 10 or 11
- Clink (standalone or with Cmder)
- Oh My Posh (optional, for modern prompts)
- Windows Terminal (recommended)

---

## Install FNM (Using winget)

```powershell
winget install Schniz.fnm
```

Verify installation:

```cmd
fnm --version
```

---

## Setup for CMD with Clink and Oh My Posh

### Step 1: Create `fnm_env.cmd` Script

Instead of capturing static output, create a wrapper that evaluates `fnm env` each time CMD loads.

Create the file:

```text
%USERPROFILE%\fnm_env.cmd
```

Paste this content:

```cmd
@for /f "tokens=*" %%i in ('fnm env') do @call %%i
```

> This ensures the environment variables are always current and avoids hardcoding paths.

---

### Step 2: Hook FNM into Clink

Create or edit the file:

```text
%LOCALAPPDATA%\clink\fnm_init.lua
```

Paste this Lua code:

```lua
local fnm_env_cmd = os.getenv("USERPROFILE") .. "\\fnm_env.cmd"

-- Check if file exists before calling
local file = io.open(fnm_env_cmd, "r")
if file then
    file:close()
    -- Call quietly without printing anything to the screen
    os.execute('cmd /c "@call "' .. fnm_env_cmd .. '" >nul 2>&1"')
else
    print("Failed to load fnm_env.cmd")
end
```

Clink will now run this automatically when launching CMD.

---

## Verify Setup

Open CMD and run:

```cmd
fnm list
node -v
```

You should see installed Node versions and the active version.

---

## Optional: PowerShell Integration

If you use PowerShell too, add this to your PowerShell profile:

```powershell
Invoke-Expression (&fnm env --use-on-cd)
```

> Profile path (editable with `notepad`):
>
> ```powershell
> notepad $PROFILE
> ```

Save and restart PowerShell to activate.
