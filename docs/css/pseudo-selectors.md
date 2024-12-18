# Pseudo Class Selectors

## Parent Selector

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Targets a parent element if child or descendant element matching a condition.

    ---

    === "CSS"

        ```css
            /* Rule applies to the <th> element only if it contains a descendant element with the class col-title class  */
            th:has(.col-title) {
                width: 300px;
            }
        ```

    === "HTML"

        ```html hl_lines="1"
            <th>
                <span class="col-title">Title</span>
            </th>
        ```
