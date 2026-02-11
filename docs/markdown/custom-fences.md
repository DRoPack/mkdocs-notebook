# Custom Fences

An overview of the custom fences created for documenting HTTP calls in `Material for MkDocs`.  This feature will allow for a `Swagger` like display of API calls in markdown using code blocks with specific syntax.  

## Example

``` markdown title="Syntax"

    ``` httpCall

        Method= GET

        Path
        _blotter.sharePoint/api/GetNames/{name}

        Header
        {
            "Accept" : ""application/json;odata=nometadata""
        }

            body
        {
            "key": "value"
        }
    ```

```

**Output**

``` httpCall

    method=POST

    path
    _api/web/lists/post-example

    header
    {
        "content-type": "application/json;odata=verbose",
        "accept": "application/json;odata=nometadata"
    }

    body
    {
        "key" : "value"
    }
```

Toggle the arrow to the right of the endpoint path to display the header and body (if included)

## Usage

The first line should contain 3 backtick (`) characters followed by httpCall, then the last line should contain the same number of backticks.

```md
    ```httpCall

    ```
```

Next to construct the body of the `httpCall` code block, we will be covering:

- Method
- Path
- Header
- Body

!!! Warning
    Each section of the code block requires a carriage return and indented by four spaces.

### Methods

To pick the method of the HTTP call, write `method=<method>` on the next line of the code block.  The options for `<method>` are GET, POST, PUT, PATCH, and DELETE.  If the method line is skipped, it will default to GET.  

```md
    ```httpCall

       method=DELETE

    ```
```

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `GET`       | <button class="method--button method--get">GET</button>     #61affe   |
| `POST`      | <button class="method--button method--post">POST</button>    #49cc90  |
| `PUT`       | <button class="method--button method--put">PUT</button>    ##fca130 |
| `PATCH`     | <button class="method--button method--patch">PATCH</button>    #af01d9 |
| `DELETE`    | <button class="method--button method--delete">DELETE</button>    #f93e3e |

### Path

Next type`path`, then on the next line enter the api endpoint.

```md
    ```httpCall

       method=DELETE

       path
       _api/web/lists/endpoint-path

    ```
```

### Header (optional)

Type `header`, then on the next line enter header information. This is optional, if left blank the header section will not appear in the custom fence layout.

```md
    ```httpCall

       method=DELETE

       path
       _api/web/lists/endpoint-path

       header
       {
        "key" : "value"
       }

    ```
```

### Body (optional)

Type `body`, then on the next line enter the body information.  This is optional, if left blank the body section will not appear in the custom fence layout.

```md
    ```httpCall

       method=DELETE

       path
       _api/web/lists/endpoint-path

       header
       {
        "key" : "value"
       }

       body
       {
        "key" : "value"
       }

    ```
```

## Configuring Custom Fences

Custom Fences Files

- [custom_fences.py](../assets/python/custom_fences.py)
- [custom_fences.css](../assets/css/custom_fences.css)
- [custom_fences.js](../assets/js/custom_fences.js)

Add markdown extension for custom super fences

```markdown title="mkdocs.yml"
    markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: httpCall
          class: http
          format: !!python/name:docs.assets.python.custom_fences.httpCall
```

While configuring the custom fences, the following error was encounter both locally while using `mkdocs serve` and when deploying to GitHub Pages.  The custom fences module was not able to be found. Both issues were related to the module not being added to the `PYTHONPATH`.  

!!! failure
    Message
    Error: MkDocs encountered an error parsing the configuration file: while constructing a Python object cannot find module 'custom_fences' (No module named 'custom_fences')

### Add Path

1. Activate Virtual Environment

    === ":fontawesome-brands-windows: **Windows**"

        ```cmd title="PowerShell"
        # Activate the virtual environment
        venv\Scripts\activate.bat
        ```

2. Set `PYTHONPATH`

    === ":fontawesome-brands-windows: **Windows**"

        ```cmd title="PowerShell"
        # Ensure `PYTHONPATH` is set in the current session
        $env:PYTHONPATH = "C:\{User\Path}\source\repos\mkdocs\mkdocs-notebook"
        ```

3. Check `PYTHONPATH`

    === ":fontawesome-brands-windows: **Windows**"

        ```cmd title="PowerShell"
        # Confirm it’s set correctly
        $env:PYTHONPATH
        ```

!!! info
    These steps will need repeated each time the virtual environment is closed

### GitHub Actions Workflow

Updating the GitHub Actions Workflow for MkDocs Deployment

Update your `.github/workflows/ci.yml` workflow file to ensure it correctly handles dependencies and sets the `PYTHONPATH` to include your custom module. Here’s how you can modify your existing `.github/workflows/ci.yml`:

1. **Add a `requirements.txt` file**:
    - Create a `requirements.txt` file in the root of your repository (if you haven’t already) with the necessary dependencies:

    ```plaintext
    mkdocs
    mkdocs-material
    pymdown-extensions
    ```

2. **Update your `.github/workflows/deploy.yml`**:
    - Modify your `.github/workflows/deploy.yml` to set the `PYTHONPATH` and install dependencies from `requirements.txt`.

    ```yaml title="GitHub Workflow  File"

    name: ci

    on:
    push:
        branches:
        - master
        - main

    permissions:
    contents: write

    jobs:
    deploy:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v4
        
        - name: Configure Git Credentials
            run: |
            git config user.name github-actions[bot]
            git config user.email 41898282+github-actions[bot]@users.noreply.github.com
        
        - uses: actions/setup-python@v5
            with:
            python-version: 3.x
        
        - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV
        
        - uses: actions/cache@v4
            with:
            key: mkdocs-material-${{ env.cache_id }}
            path: .cache
            restore-keys: |
                mkdocs-material-
        
        - name: Install dependencies
            run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt
        
        - name: Set PYTHONPATH
            run: |
            export PYTHONPATH=$PYTHONPATH:$GITHUB_WORKSPACE/docs/assets/python
            echo "PYTHONPATH=$PYTHONPATH" >> $GITHUB_ENV
        
        - name: Deploy to GitHub Pages
            run: mkdocs gh-deploy --force

    ```

**Explanation of the Updated Steps**

1. **Install Dependencies**:
    - This step ensures all dependencies listed in `requirements.txt` are installed, which includes `mkdocs`, `mkdocs-material`, and any other packages you may have listed.

2. **Set PYTHONPATH**:
    - This step sets the `PYTHONPATH` environment variable to include your custom module path (`docs/assets/python`). The path is then exported to the GitHub Actions environment.

3. **Deploy to GitHub Pages**:
    - The `mkdocs gh-deploy --force` command is run to deploy the site.
