
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

## TypeScript Definitions

```cmd
npm info @types/jquery
```

- Provides information about TypeScript definitions for the specified package. It’s recommended to use a version that matches the installed npm package closely.

```cmd
npm show @types/jquery versions --json
```

- Displays all available versions of the specified package’s TypeScript definitions in JSON format, preventing truncation of the version list.
