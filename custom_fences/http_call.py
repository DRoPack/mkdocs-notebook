from itertools import count

# Create a counter
counter = count()

def generate_unique_id():
    # Get the next value from the counter
    return next(counter)


def httpCall(source, language, class_name, options, md, **kwargs):
    # Splitting the code block into lines
    lines = source.split('\n')

    # Extracting the block name from the first line
    block_name = lines[0].strip()

    # Initializing method as None
    method = None

    # Iterating through the rest of the lines to extract parameters
    for line in lines[1:]:
        # Stripping whitespace from the line
        line = line.strip()

        # Checking if the line starts with 'method='
        if line.startswith('method='):
            # Extracting the method value
            method = line.split('=')[1]
            break
    else:
        # If the loop completes without finding 'method=', set a default value
        method = "GET"

    # Initialize variables for path, headers, and body
    path = ""
    headers = ""
    body = ""
    response = ""
    
    # Iterate through each line and extract relevant sections
    current_section = None
    for line in lines:
        if line.strip().lower() == 'path':
            current_section = 'path'
        elif line.strip().lower() == 'header':
            current_section = 'header'
        elif line.strip().lower() == 'body':
            current_section = 'body'
        elif line.strip().lower() == 'response':
            current_section = 'response'

        elif current_section == 'path':
            path += line.rstrip() + "\n"
        elif current_section == 'header':
            headers += line.rstrip() + "\n"
        elif current_section == 'body':
            body += line + "\n"
        elif current_section == 'response':
            response += line + "\n"
    
    # Remove trailing newlines from sections
    path = path.strip()
    headers = headers.strip()
    body = body.rstrip()
    response = response.rstrip()

    # Generating a unique ID for each input
    input_id = f"{generate_unique_id()}"
    
    # Initialize HTML markup
    html = f"""
    <div class="swagger-ui">
        <div class="opblock opblock-{method.lower()}">
    """
    
    # Add path section if not empty
    if path:
        html += f"""
        <!-- Method and Path -->
        <div class="opblock-summary opblock-summary-{method.lower()}">
            <button class="opblock-summary-control"> 
                <span class="opblock-summary-method">{method.upper()}</span>
                <pre class="opblock-summary-path"><code class="lang-html">{path}</code></pre>
                <svg class="arrow" width="20" height="20" aria-hidden="true" focusable="false"xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.418 6.109c.272-.268.709-.268.979 0s.271.701 0 .969l-7.908 7.83c-.27.268-.707.268-.979 0l-7.908-7.83c-.27-.268-.27-.701 0-.969.271-.268.709-.268.979 0L10 13.25l7.418-7.141z"></path>
                </svg>
            </button>
        </div>
        """
    
    # Add section for Header and Response Body

    html += f"""
        <!-- Header and Response Body -->
        <div class="opblock-body">
            <div class="opblock-section">
    """

    # Add headers section if not empty
    if headers:
        html += f"""
        <!-- Header -->
                <div class="header-wrapper">
                    <div class="opblock-section-header">Headers</div>
                    <div class="opblock-request-body">
                        <pre class="body-param"><code class="lang-json">{headers}</code></pre>
                    </div>
                </div>
        """
    
    # Add body section if not empty
    if body:
        html += f"""
        <!-- Body -->
                <div class="header-wrapper">
                    <div class="opblock-section-body">Body</div>
                    <div class="opblock-request-body">
                        <pre class="body-param"><code class="lang-json">{body}</code></pre>
                    </div>
                </div>
        """

    # Add response section if not empty
    if response:
        html += f"""
        <!-- Response -->
                <div class="header-wrapper">
                    <div class="opblock-section-body">Response</div>
                    <div class="opblock-request-body">
                        <pre class="body-param"><code class="lang-json">{response}</code></pre>
                    </div>
                </div>
        """
    
    # Close the HTML markup
    html += """
            </div> <!-- End section-->
        </div> <!--End body -->
    </div> <!-- End method container -->
</div> <!--End swagger ui -->
"""
    
    # Return the formatted HTML
    return html