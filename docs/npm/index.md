
# NPM Commands

Below is a list of commonly used NPM commands along with their descriptions. These are useful for managing packages in your projects effectively.

## Global Package Listing

```cmd
npm list -global --depth=0
```

- Lists all globally installed packages without displaying their dependencies.

## Package Information

```cmd
npm info jquery
```

- Displays detailed information about the specified npm package, including its release history, available versions, and more.

```cmd
npm info @types/jquery
```

- Provides information about TypeScript definitions for the specified package. It’s recommended to use a version that matches the installed npm package closely.

```cmd
npm show @types/jquery versions --json
```

- Displays all available versions of the specified package’s TypeScript definitions in JSON format, preventing truncation of the version list.

## Installing Packages

```cmd
npm install jquery
```

- Installs the latest version of the specified package into the project.

```cmd
npm install jquery@1.12.4
```

- Installs a specific version of the specified package.

```cmd
npm install jquery --save
```

- Installs the package and saves it to the `dependencies` list in the `package.json` file.

## NPM Versioning Characters Explained

Here is a comprehensive table explaining the various characters and notations used in npm versioning:

| **Character/Notation** | **Example**         | **Meaning**                                                                                     | **Version Range Example**                      |
|-------------------------|---------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------|
| **Caret (`^`)**        | `^1.10.2`          | Allows **minor and patch updates**, keeping the **major version the same**.                     | `1.10.2` to `<2.0.0`                          |
| **Tilde (`~`)**        | `~1.10.2`          | Allows **patch updates only**, keeping the **minor version the same**.                         | `1.10.2` to `<1.11.0`                         |
| **Exact Version**      | `1.10.2`           | Installs the **specific version only**.                                                        | Only `1.10.2`                                 |
| **Wildcard (`x`)**     | `1.10.x`           | Matches any **patch version** for the specified **major.minor** version.                       | `1.10.0`, `1.10.1`, `1.10.5`, etc.            |
| **Wildcard (`*`)**     | `*`                | Matches **any version**. This is risky as it could include breaking changes.                   | Any available version                         |
| **Range (`-`)**        | `1.5 - 1.10`       | Installs the **latest version within the range**, inclusive.                                   | `1.5.0` to `1.10.x`                           |
| **Greater/Less Than**  | `>1.10.2`          | Installs any version **greater than** the specified version.                                   | `1.10.3`, `2.0.0`, etc.                       |
| **Greater/Less Than**  | `<2.0.0`           | Installs any version **less than** the specified version.                                      | `1.0.0` to `1.999.999`, but not `2.0.0`       |
| **Logical Ranges**     | `>=1.10.2 <2.0.0`  | Combines range operators to define a **specific range of versions**.                          | `1.10.2` to `<2.0.0`                          |

---

## Example Command Breakdown

#### Command

```bash
npm install @types/jquery@1.10.x --save-dev
```

#### Explanation

1. **`@types/jquery`**: The package name (scoped under `@types` for TypeScript definitions).
2. **`@1.10.x`**: Installs the latest patch version within the `1.10` minor version (e.g., `1.10.5`).
3. **`--save-dev`**: Adds the package to the `devDependencies` in your `package.json`.
