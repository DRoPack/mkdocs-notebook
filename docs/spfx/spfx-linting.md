# Linting Setup

## Prettier

Recommended configuration for `Prettier`

Create `.prettierrc` file in the root of the project

```json title=".prettierrc"
  {
    "singleQuote": true,
    "tabWidth": 2,
    "semi": true,
    "trailingComma": "es5",
    "printWidth": 80
  }
```

## TS Lint

Recommended configuration for `TS lint`

Add the following to the base settings for the `tslint.json` file

```json title="tslint.json"
    "trailing-comma": [
      false,
      {
      "multiline": "always",
      "singleline": "never"
      }
    ],
    "comma-dangle": "off"
```
