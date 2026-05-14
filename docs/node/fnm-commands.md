# FNM Commands

This is a quick reference guide for `fnm` (Fast Node Manager).

| FNM Commands                  | Notes                                            |
| ----------------------------- | ------------------------------------------------ |
| `fnm -V`                      | Capital `V` in `fnm` to view fnm version         |
|                               |                                                  |
| `fnm list` or `fnm ls`        | Lists installed Node versions                    |
| `fnm list-remote`             | See all available Node.js versions               |
|                               |                                                  |
| `fnm install latest`          | Installs latest Node version                     |
| `fnm install X.Y.Z`           | Installs specific version                        |
| `fnm install --lts`           | Installs latest LTS version                      |
|                               |                                                  |
| `fnm use X.Y.Z`               | Switches to specific version                     |
| `fnm default X.Y.Z`           | Sets default Node version                        |
| `fnm alias 1.4.0 SP2019`      | Sets shortcut name for `fnm use SP2019`          |
|                               |                                                  |
| `fnm uninstall X.Y.Z`         | Uninstalls specific version                      |

---

## How to install $$

### macOS and Linx

Install FNM using the install script or Homebrew:

```cmd
# option 1: install script
curl -fsSL https://fnm.vercel.app/install | bash

# option 2: Homebrew
brew install fnm
```

After installing, add the following to your shell profile (.zshrc, .bashrc, or .profile) to initialize FNM in each new terminal session:

```cmd
eval "$(fnm env)"
```

### Windows

Install FNM using winget:

```cmd
winget install Schniz.fnm
```

## Automatic version switching

One of FNM’s standout features is automatic version switching. When you have a `.node-version` or `.nvmrc` file in your project’s root folder, FNM will automatically switch to the specified Node.js version when you navigate into that directory.

To create a .node-version file in your project root, use the following command. Once present, FNM will automatically switch to the specified version when you navigate into the directory:

```cmd
cd ~/dev/spfx-hello-world
# create the version file
node -v > .node-version
```

## Migration Clean up

After successfully migrating to FNM, make sure to clean up your old installation. This prevents conflicts and ensures a clean development environment.

Delete your old .nvm folder:

- On macOS: `rm -rf ~/.nvm`
- On Windows: Remove the NVM installation directory (typically `C:\Users\<username>\AppData\Roaming\nvm`) and its associated nodejs symlink folder

Also update your shell profile (.zshrc, .bashrc, or .profile) to remove the old NVM initialization scripts and add FNM instead.

## Additional Notes

- `fnm` is generally faster and more lightweight than `nvm`.
- It supports automatic version switching via `.nvmrc` or `.node-version` files if enabled.

For more details, visit the [FNM GitHub repo](https://github.com/Schniz/fnm).
