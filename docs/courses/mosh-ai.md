# MOSH AI Apps

## Video 2

### What is BUN?

BUN is a modern JavaScript runtime, similar to Node.js, but faster with better built-in tooling.
Unlike Node.js, BUN bundles several tools together out of the box:

- NPM
- ts-node
- nodemon

| Includes    |             |
|------------|------------|
| Runtime | Package Manager|
| Task Runner | TypeScript Transpiler|

- [x] <https://bun.sh>

```powershell title="Install on Windows"
powershell -c "irm bun.sh/install.ps1 | iex"
```

!!! warning
    Important Note (Starting with BUN v1.3.2) isolated installs become the default.
    Mosh’s course uses **hoisted installs** (Node-style), so we need to explicitly enable that.

- [x] <https://bun.com/docs/pm/cli/install#installation-strategies>

```bash title="Install linker hoisted"
bun install --linker hoisted
```

---

## Video 3

### Creating the Project Structure

1. Create the project folder

    ```text
    c:\repos\ai-apps\mosh-ai-app
    ```

2. Initialize BUN

    ```bash
    bun init
    ```

3. Select **Blank**

4. Open in VS Code

    ```bash
    code .
    ```

5. Delete the `cursor` file

6. Create folders

    ```text
    packages/
    packages/client
    packages/server
    ```

7. Update `package.json` with workspaces

=== "Standard Syntax

    ```json
    "workspaces": [
    "packages/client",
    "packages/server"
    ]
    ```

=== "Shorthand Syntax

    ```json
        "workspaces": ["packages/*"]
    ```

## Video 4

### Creating the Backend

```bash
cd packages/server
bun init
bun add express
bun add -d @types/express
```

Create `server/index.ts` and set up Express.

Run the server:

```bash
bun run index.ts
```

Update `server/package.json`:

```json
"scripts": {
  "start": "bun run index.ts",
  "dev": "bun --watch run index.ts"
}
```

Run dev:

```bash
bun run dev
```

---

## Video 5

### Managing OpenAI API Key

```bash
bun add dotenv
```

Create file:

```text
server/.env
```

---

## Video 6

### Creating the Frontend

Using **Vite**

```bash
cd packages/client
bun create vite .
bun install
```

Prompts:

- React
- TypeScript

---

## Video 7

### Connecting Frontend and Backend

Add to `server/index.ts`:

```ts
app.get('/api/hello', (req, res) => {
  res.json({ message: "Hello World!" })
});
```

Test:

```url
http://localhost:3000/api/hello
```

---

## Video 8

### Running Both Apps Together

From the root:

```bash
bun add -d concurrently
```

Create `/index.ts`:

```ts
import concurrently from 'concurrently';

concurrently([
  {
    name: 'server',
    command: 'bun run dev',
    cwd: 'packages/server',
    prefixColor: 'cyan'
  },
  {
    name: 'client',
    command: 'bun run dev',
    cwd: 'packages/client',
    prefixColor: 'green'
  }
]);
```

Update root `package.json`:

```json
"scripts": {
  "dev": "bun run index.ts"
}
```

---

## Video 9

### Setting up TailwindCSS

Docs: <https://tailwindcss.com/docs/installation/using-vite>

```bash
cd packages/client
bun add tailwindcss @tailwindcss/vite
```

Update `vite.config.ts`:

```ts
import tailwindcss from '@tailwindcss/vite';

plugins: [react(), tailwindcss()]
```

Update `index.css`:

```css
@import "tailwindcss";
```

VS Code Extension:

- Tailwind CSS IntelliSense

Update `App.tsx`:

```tsx
return <p className="font-bold">{message}</p>
```

---

## Video 10

### Setting up Shadcn

<https://ui.shadcn.com/docs/installation/vite>

- Skipped the first couple setup steps since these were setup during TailwindCSS configuration

Update `packages/client/tsconfig.json`

```json
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
```

Update `packages/client/tsconfig.app.json`

```json
// Add inside the compilerOptions object
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },  
```

```json
// Run from packages/client folder
bun add -D @types/node
```

Update `packages/client/vite.config.ts`

```ts
// Add import
import path from 'path'

// Add resolve property inside the defineConfig
resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  ```
  
  Run `shadcn` init command to setup project

  ```json
// Run from packages/client folder
bunx --bun shadcn@latest init

// Color prompt - is the base colors for components
  ```

#### Install Components

<https://ui.shadcn.com/docs/components>

  ```json
// Run from packages/client folder
bunx --bun shadcn@latest add button
```

#### Usage

Update `App.tsx`

```tsx
  return (
    <div className="p-4">
      <p className="font-bold text-3xl">{message}</p>
      <Button>Click Me</Button>
    </div>
  );
  ```

## Video 11

### Setting up Prettier

- Install `Prettier` VSCode extension
- Create `.prettierrc` file in the root of the project

```json
// Basic configuration
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 3
}
```

From VSCode settings `Ctrl+,` ensure Prettier set as default formatter `FormatOnSave`

#### Format from CommandLine

- Install `Prettier` as development dependency to the the project

```json
// Run from the root of project
bun run -d prettier
```

- Navigate `package.json`
- Add script parameter

```json
"script": {
    // Other scripts...
    // --write . means start from current directory (root)
    "format": "prettier --write ."
}
```

- Add file `.prettierignore` in the root of the project

```json
node_modules
bun.lock
```

- Running formatting

```json
// Run from root of project
bun run format
```

## Video 12

### Setting up Husky

- Runs formatting prior to commits in VSCode.  
- MOSH indicated their was an issue running bunx command at time of video release
- **Maybe revist this**
