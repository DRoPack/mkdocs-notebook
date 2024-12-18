# :fontawesome-brands-css3-alt: CSS: Concepts and Examples

## Table of Contents

<div class="grid cards" markdown>

- :octicons-arrow-right-24: [__Attribute Selectors__] [attribute-selectors]
- :octicons-arrow-right-24: [__Combinators__] [combinators]
- :octicons-arrow-right-24: [__Pseudo Selectors__] [pseudo-selectors]
- :octicons-arrow-right-24: [__Box-Sizing__] [box-sizing]

</div>

[attribute-selectors]: attribute-selectors.md
[combinators]: combinators.md
[pseudo-selectors]: pseudo-selectors.md
[box-sizing]: #box-sizing

---

## Box-Sizing

`box-sizing` is a CSS property used to define how the total width and height of an element are calculated. It controls whether the padding and border are included in the element's dimensions or not. A best practice is to apply it as a universal selector to set the default behavior for the entire `HTML` document.

=== "CSS"

    ```css
    element {
        box-sizing: border-box;
    }

    /* Set universal selector  */
    * {
        box-sizing: border-box;
    }
    ```
