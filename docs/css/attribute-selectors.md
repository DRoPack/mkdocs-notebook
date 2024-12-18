# Attribute Selectors

## Exact Match (=)

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets elements with an attribute value exactly matching the specified value.

    ---

    === "CSS"

        ```css
            a[href="https://example.org"] {
                color: green;
            }
        ```

    === "HTML"

        ```html hl_lines="1"
            <a href="https://example.org">SELECTED</a>
            <a href="https://example.com">not selected</a>
        ```

## Contains (*=)

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets elements with an attribute value containing the specified substring.

    ---

    === "CSS"

        ```css
            a[href*="example"] {
                font-size: 2em;
            }
        ```

    === "HTML"

        ```html hl_lines="1 2 3"
            <a href="https://example.org">SELECTED</a>
            <a href="https://example.com">SELECTED</a>
            <a href="https://MyExample.com">SELECTED</a>
            <a href="https://sample.org">not selected</a>
        ```

## Ends With ($=)

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets elements with an attribute value ending with the specified substring.

    ---

    === "CSS"

        ```css
            a[href$=".org"] {
                font-style: italic;
            }
        ```

    === "HTML"

        ```html hl_lines="1"
            <a href="https://example.org">SELECTED</a>
            <a href="https://example.com">not selected</a>
        ```

## Contains Word (~=)

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets elements with an attribute value containing the specified word (space-separated).

    ---

    === "CSS"

        ```css
            a[class~="logo"] {
                padding: 2px;
            }
        ```

    === "HTML"

        ```html hl_lines="1 2"
            <a class="logo">SELECTED</a>
            <a class="main logo">SELECTED</a>
            <a class="logoman">Not Applied</a>
        ```

## Attribute Exists

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets elements that have the specified attribute, regardless of its value.

    ---

    === "CSS"

        ```css
            a[title] {
                color: purple;
            }
        ```

    === "HTML"

        ```html hl_lines="1"
            <a title="tooltip">SELECTED</a>
            <a>not selected</a>
        ```

## Override Inline Styles

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets elements with inline styles, useful for overriding them.

    ---

    === "CSS"

        ```css
            a[style] {
                height: 2px !important;
            }
        ```

    === "HTML"

        ```html hl_lines="1"
            <a style="color: red;">SELECTED</a>
            <a>not selected</a>
        ```

    === "SharePoint Calendar" 

        ```css hl_lines="6"
            /* /manufacturing/SitePage/buildingschedule.aspx - overrides inline heights for calendar  */
            .ms-acal-item[style] {
                height: 19px !important;
            }

            <div class="ms-acal-item" style="height: 10px;">SELECTED</div>
        ```
