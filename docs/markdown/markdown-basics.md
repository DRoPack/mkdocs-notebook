# Markdown Basics

## Headers

| Syntax   | Result              | Syntax      | Result                 |
| -------- | ------------------- | ----------- | ---------------------- |
| `# H1`   | # Heading level 1   | `#### H4`   | #### Heading level 4   |
| `## H2`  | ## Heading level 2  | `##### H5`  | ##### Heading level 5  |
| `### H3` | ### Heading level 3 | `###### H6` | ###### Heading level 6 |

## Emphasis

| Syntax                           | Result                         |
| -------------------------------- | ------------------------------ |
| `*Italic text* or _italic text_` | _Italic text_ or _italic text_ |
| `**Bold text** or __bold text__` | **Bold text** or **bold text** |
| `~~Strikethrough text~~`         | ~~Strikethrough text~~         |

## Escaping Characters

```markdown title="Syntax"
\*This text is not italicized\*
```

## Highlight

```markdown title="Syntax"
Highlight ==words to get an A== in markdown
```

> Result

Highlight ==words to get an A== in markdown

## Paragraphs

| Syntax                                                           | Result                                                                        |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `Random thoughts in markdown.`                                   | Random thoughts in markdown.                                                  |
| `Add content to your markdown.<br>Then break over several ines.` | Add more content to your markdown page.<br>Then break that over several ines. |

!!! tip

    Adding a **`<br>`** to insert line breaks into paragraphs is the preferred method.  Double space (or more) will add a line break known as trailing whitespace, but **`<br>`** conveys clearly the intent for a line break.

## Blockquotes

```markdown
> This is a blockquote.
```

> This is a blockquote.

```markdown
> This is a blockquote.<br> You can write multiple lines.
```

> This is a blockquote.<br> You can write multiple lines.

## Links

| Syntax                                 | Result                               |
| -------------------------------------- | ------------------------------------ |
| `[Link to OpenAI](https://openai.com)` | [Link to OpenAI](https://openai.com) |
| `<https://openai.com>`                 | <https://openai.com>                 |
| `<fake@example.com>`                   | <fake@example.com>                   |
| `[Email Me](fake@example.com)`         | [Email Me](fake@example.com)         |
| `[Escaping Charaters](#escaping-charaters)`  | [Escaping Characters](#escaping-characters)    |

### Reference-style Links

Reference style links provide a way to keep markdown clean by inserting a reference to a link somewhere else in the markdown file.

```markdown title="Syntax"
Keep your [long links][link-openai] out of my text!!

[link-openai]: https://openai.com
```

> Result:<br> Keep your [long links][link-openai] out of my text!!

[link-openai]: https://openai.com

## Lists

### Unordered List

```markdown title="Syntax"
- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2
```

### Ordered List

```markdown title="Syntax"
1. First item
2. Second item
   1. Subitem 2.1
   2. Subitem 2.2
```

## Images

| Syntax                                               | Result                                             |
| ---------------------------------------------------- | -------------------------------------------------- |
| `![web image](https://picsum.photos/100)`            | ![picsum-web image](https://picsum.photos/100)     |
| `![local image](../assets/img/markdown/example.jpg)` | ![local image](../assets/img/markdown/example.jpg) |

## Code

Inline `code` can be inserted using backticks.

## Code block

````title="Syntax"

``` javascript
function name(yourName) {
  const myName = `Hi, my name is ${yourName}`;
}
```

````

```javascript title="Result"
function name(yourName) {
  const myName = `Hi, my name is ${yourName}`;
}
```

````title="Syntax"

``` css
#id {
    color: green;
}

.my-class {
    background-color: lime;
}
```
````

```css title="Result"
#id {
  color: green;
}

.my-class {
  background-color: lime;
}
```

!!! Info

    List of <a href="https://github.com/jincheng9/markdown_supported_languages?tab=readme-ov-file#heres-a-full-list-of-supported-languages" target='_blank'>supported languages</a> for code blocks

## Tables

```markdown title="Syntax"
| Name  | Age |
| ----- | --- |
| Alice | 30  |
| Bob   | 35  |
| Carol | 25  |
```

> Result

| Name  | Age |
| ----- | --- |
| Alice | 30  |
| Bob   | 35  |
| Carol | 25  |

## Horizontal Rule

```markdown title="Syntax"
---
```

## Task Lists

```markdown title="Syntax"
- [x] Task 1
- [ ] Task 2
- [ ] Task 3
```
