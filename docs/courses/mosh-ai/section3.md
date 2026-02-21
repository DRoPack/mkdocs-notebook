---
title: Section 3 - Setting Up Modern Full Stack Project
---

<!-- markdownlint-disable MD046 -->
<!-- markdownlint-disable MD007 -->

### Video 2 — What is BUN?

BUN is a modern JavaScript runtime, similar to Node.js, but faster with better built-in tooling.
Unlike Node.js, BUN bundles several tools together out of the box:

- NPM
- ts-node
- nodemon

| Includes    |                       |
| ----------- | --------------------- |
| Runtime     | Package Manager       |
| Task Runner | TypeScript Transpiler |

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

### Video 3 — Creating the Project Structure

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

   === "Standard Syntax"

       ```json
       "workspaces": [
       "packages/client",
       "packages/server"
       ]
       ```

   === "Shorthand Syntax"

       ```json
       "workspaces": ["packages/*"]
       ```

---

### Video 4 — Creating the Backend

#### Initialize the Server

```bash
cd packages/server
bun init
bun add express
bun add -d @types/express
```

#### Create the Express App

Create `server/index.ts` and set up your Express server.

#### Run the Server

```bash
bun run index.ts
```

#### Update `package.json`

Add scripts for running and developing:

```json
{
 "scripts": {
  "start": "bun run index.ts",
  "dev": "bun --watch run index.ts"
 }
}
```

#### Run in Development Mode

```bash
bun run dev
```

---

### Video 5 — Managing API Key

```bash
bun add dotenv
```

Create file `server/.env`.

---

### Video 6 — Creating the Frontend

Using **Vite**:

```bash
cd packages/client
bun create vite .
bun install
```

Prompts:

- React
- TypeScript

---

### Video 7 — Connecting Frontend and Backend

Add to `server/index.ts`:

```ts
app.get('/api/hello', (req, res) => {
 res.json({ message: 'Hello World!' });
});
```

Test:

```url
http://localhost:3000/api/hello
```

---

### Video 8 — Running Both Apps Together

From the root:

```bash
bun add -d concurrently
```

Create `index.ts` in the root:

```ts
import concurrently from 'concurrently';

concurrently([
 {
  name: 'server',
  command: 'bun run dev',
  cwd: 'packages/server',
  prefixColor: 'cyan',
 },
 {
  name: 'client',
  command: 'bun run dev',
  cwd: 'packages/client',
  prefixColor: 'green',
 },
]);
```

Update root `package.json`:

```json
"scripts": {
  "dev": "bun run index.ts"
}
```

---

### Video 9 — Setup TailwindCSS

Docs: [https://tailwindcss.com/docs/installation/using-vite](https://tailwindcss.com/docs/installation/using-vite)

```bash
cd packages/client
bun add tailwindcss @tailwindcss/vite
```

Update `vite.config.ts`:

```ts
import tailwindcss from '@tailwindcss/vite';

plugins: [react(), tailwindcss()];
```

Update `index.css`:

```css
@import 'tailwindcss';
```

VS Code Extension:

- Tailwind CSS IntelliSense

Update `App.tsx`:

```tsx
return <p className="font-bold">{message}</p>;
```

---

### Video 10 — Setup Shadcn

Docs: [https://ui.shadcn.com/docs/installation/vite](https://ui.shadcn.com/docs/installation/vite)

Update `packages/client/tsconfig.json`:

```json
"compilerOptions": {
  "baseUrl": ".",
  "paths": {
    "@/*": ["./src/*"]
  }
}
```

Update `packages/client/tsconfig.app.json`:

```json
// Add inside compilerOptions
"baseUrl": ".",
"paths": {
  "@/*": ["./src/*"]
}
```

Install Node types:

```bash
bun add -D @types/node
```

Update `vite.config.ts`:

```ts
import path from 'path';

resolve: {
  alias: {
    "@": path.resolve(__dirname, "./src"),
  },
},
```

Run Shadcn init:

```bash
bunx --bun shadcn@latest init
```

Install Components (example: button):

```bash
bunx --bun shadcn@latest add button
```

Update `App.tsx`:

```tsx
return (
 <div className="p-4">
  <p className="font-bold text-3xl">{message}</p>
  <Button>Click Me</Button>
 </div>
);
```

---

### Video 11 — Setup Prettier

- Install Prettier VSCode extension
- Create `.prettierrc` in project root:

```json
{
 "singleQuote": true,
 "semi": true,
 "trailingComma": "es5",
 "printWidth": 80,
 "tabWidth": 3
}
```

Ensure Prettier is default formatter with `FormatOnSave` enabled.

Install Prettier as a dev dependency:

```bash
bun add -D prettier
```

Add format script to `package.json`:

```json
"scripts": {
  "format": "prettier --write ."
}
```

Create `.prettierignore`:

```text
node_modules
bun.lock
```

Run formatting:

```bash
bun run format
```

---

### Video 12 — Setup Husky

- Runs formatting prior to commits in VSCode.
- Bunx command may have issues at video release.
- **Consider revisiting this setup later.**
