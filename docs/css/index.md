# :fontawesome-brands-css3-alt: CSS Refresher: Concepts and Examples

## Table of Contents

- [Box-Sizing](#box-sizing)

---

## Box-Sizing

`box-sizing` is a CSS property used to define how the total width and height of an element are calculated. It controls whether the padding and border are included in the element's dimensions or not. A best practice is to apply it as a universal selector to set the default behavior for the entire `HTML` document.

### Syntax

```css
element {
    box-sizing: border-box;
}

/* Set universal selector  */
* {
    box-sizing: border-box;
}
```
