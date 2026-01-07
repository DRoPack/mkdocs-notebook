# FNM Commands

This is a quick reference guide for `fnm` (Fast Node Manager).

| FNM Equivalent            | Notes                         |
|---------------------------|-----------------------------  |
| `fnm -V`                  | Capital `V` in `fnm`          |
| `fnm list` or `fnm ls`    | Lists installed Node versions |
| `fnm install latest`      | Installs latest Node version  |
| `fnm install X.Y.Z`       | Installs specific version     |
| `fnm use X.Y.Z`           | Switches to specific version  |
| `fnm install --lts`       | Installs latest LTS version   |
| `fnm default X.Y.Z`       | Sets default Node version     |
| `fnm uninstall X.Y.Z`     | Uninstalls specific version   |

---

## Additional Notes

- `fnm` is generally faster and more lightweight than `nvm`.
- It supports automatic version switching via `.nvmrc` or `.node-version` files if enabled.

For more details, visit the [FNM GitHub repo](https://github.com/Schniz/fnm).
