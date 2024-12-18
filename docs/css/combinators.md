# Combinators

## Adjacent Sibling +

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline:  Elements share the same parent

    :material-checkbox-marked-circle-outline: Second element comes immediately after the first element

    ---
    
    === "CSS"

        ```css
        h2 + p {
            color: red;
        }
        ```

    === "HTML"

        ```html hl_lines="3 8"
        <div>
            <h2>Not Applied</h2>
            <p>CSS Applied</p>
            <h2>Not Applied</h2>
            <h3>Not Applied</h3>
            <p>Not Applied</p>
            <h2>Not Applied</h2>
            <p>**CSS Applied</p>
        </div>
        ```

## General Sibling ~

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Elements share the same parent

    :material-checkbox-marked-circle-outline: Second element comes first element

    ---

    === "CSS"

        ```css
        h2 ~ p {
            color: red;
        }
        ```

    === "HTML"

        ```html hl_lines="3 6"
        <div>
            <h2>Not Applied</h2>
            <p>**CSS Applied</p>
            <h2>Not Applied</h2>
            <h3>Not Applied</h3>
            <p>**CSS Applied</p>
        </div>
        ```

## Child >

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Second element is a direct child of the first element

    ---
    
    === "CSS"

        ```css
        h2 > p {
            color: red;
        }
        ```

    === "HTML"

        ```html hl_lines="3 8"
        <div>
            <div>Not Applied</div>
            <p>**CSS Applied</p>
            <div>Not Applied</div>
            <article>
                <p>Not Applied</p>
            </article>
            <p>**CSS Applied*</p>
        </div>
        ```

## Descendant

!!! pied-piper "Definition"

    :material-checkbox-marked-circle-outline: Second element is a descendant of the first element

    ---
    
    === "CSS"

        ```css
        h2 p {
            color: red;
        }
        ```

    === "HTML"

        ```html hl_lines="3 6 8"
        <div>
            <div>Not Applied</div>
            <p>**CSS Applied</p>
            <div>Not Applied</div>
            <article>
                <p>**CSS Applied</p>
            </article>
            <p>**CSS Applied</p>
        </div>
        ```
