# VSCode Tips

## Keyboard Shortcuts


### Useful Commands

| Shortcut | Action |
|---------|---------|
| **`Ctrl + P`** | **Quick Open**. Quickly open files by name. Also supports symbols and line navigation. |
| **`Ctrl + Shift + P`** | Open the **Command Palette** |
| **`Ctrl + Shift + P`** → `TypeScript: Restart TS Server` | Restart TypeScript Server |
| **`Ctrl + Shift + P`** → `Developer: Reload Window` | Reload VS Code Window |
| **`Ctrl + Shift + P`** → `Preferences: Open User Settings (JSON)` | Open Settings (JSON) |
| **`Shift + Alt + F`** | Format Current File |
| **`Ctrl + ` ` (backtick)** | Toggle Terminal |
| **`Ctrl + Shift + F`** | Find Across Files |
| **`F12`** | Go to Definition |
| **`Alt + F12`** | Peek Definition |
| **`Ctrl + Shift + M`** | Show Problems Panel |

---

### Editing & Selection

| Shortcut | Purpose |
|-----------|-----------|
| **`Ctrl + D`** | Select next occurrence of the current word |
| **`Ctrl + Shift + L`** | Select all occurrences of the current selection |
| **`Shift + Alt + →`** | Expand selection (word → statement → block → function) |
| **`Shift + Alt + ←`** | Shrink selection |
|  |  |
| **`Alt + Click`** | Add additional cursors with the mouse |
| **`Ctrl + Alt + ↓`** / **`Ctrl + Alt + ↑`** | Add cursor below or above |
| **`Shift + Alt + Drag`** | Column (box) selection across multiple lines |
| **`Ctrl + U`** | Undo last cursor operation |
|  |  |
| **`Shift + Alt + ↓`** | Duplicate line below |
| **`Shift + Alt + ↑`** | Duplicate line above |
| **`Alt + ↓`** / **`Alt + ↑`** | Move line down or up |
|  |  |
| **`Ctrl + /`** | Toggle line comment |
| **`Shift + Alt + A`** | Toggle block comment |

---

## Code Snippets

Create snippets for only a specific language.

#### Create a Language-Specific Snippet

1. Press `Ctrl + Shift + P`
2. Select **Snippets: Configure Snippets**
3. Choose a language:
    - JavaScript
    - TypeScript
    - Markdown
    - PowerShell

4. VS Code creates or opens the appropriate snippet file.


```text title="Snippet file name examples"
typescript.json
powershell.json
markdown.json
// Project-specific language ID
python-markdown.json
```

!!! note
    Snippet files are created based on the language ID. If an extension introduces a custom language ID, a specific snippet file will need to be created such as `python-markdown.json` instead of the standard `markdown.json`.


```json title="Example snippet file content"
{
  "Console Log": {
    "prefix": "cl",
    "body": [
      "console.log('$1');"
    ],
    "description": "Console log statement"
  }
}
```


#### VS Code Snippet Variables

| Syntax | Purpose | Example |
|----------|----------|----------|
| **`$0`** | Final cursor position after all tab stops are completed | `"$0"` |
| **`$1`** | First tab stop | `"console.log($1);"` |
| **`$2`** | Second tab stop | `"const $1 = $2;"` |
| **`${1:text}`** | Tab stop with default value | `"${1:cards}"` |
| **`${2:url}`** | Named placeholder | `"![${1:alt text}](${2:url})"` |
| **`${1\|a,b,c\|}`** | Dropdown list of values | `"${1\|js,json,ts,css,powershell,text\|}"` |
| **`$1 ... $2 ... $3`** | Sequential tab navigation | Press `Tab` to move through placeholders |
| **Same tab stop reused** | Update multiple locations at once | `"${1:Name} - ${1:Name}"` |
| **`\\$`** | Literal dollar sign | `"\\$100"` |
| **`\\}`** | Literal closing brace | `"\\}"` |


```json title="Snippets not appearing"
// In settings.json add
"[markdown]": {
    "editor.quickSuggestions": {
      "other": "on",
      "comments": "off",
      "strings": "off",
    }
}
```
