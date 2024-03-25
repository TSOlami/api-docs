import re
import os


def get_flask_endpoint_examples():
    """
    Ask the user to provide examples of how their flask API endpoints are defined in the codebase.
    """

    print("Please provide examples of how your Flask API endpoints are defined.")
    print("For example, you can provide lines of code that define an endpoint using decorators like @app.route, @server.route, etc.")
    
    # Initialize list of examples
    flask_endpoint_examples = []

    # Get examples from user
    while True:
        example = input("Enter an example and press enter. Enter 'done' when you are finished: ").strip()
        if example == 'done':
            break
        flask_endpoint_examples.append(example)

    print(f"{len(flask_endpoint_examples)} examples provided.")
    return flask_endpoint_examples

def get_express_endpoint_examples():
    """
    Ask the user to provide examples of how their Express API endpoints are defined in the codebase.
    """

    print("Please provide examples of how your Express API endpoints are defined.")
    print("For example, you can provide the route function with all the http methods like router.get, router.post, app.put, server.delete, etc.")
    
    # Initialize list of examples
    express_endpoint_examples = []

    # Get examples from user
    while True:
        example = input("Enter an example and press enter. Enter 'done' when you are finished: ").strip()
        if example == 'done':
            break
        express_endpoint_examples.append(example)

    print(f"{len(express_endpoint_examples)} examples provided.")
    return express_endpoint_examples

def get_decorator_used(line, endpoint_examples):
    """
    Dynamically find the decorator used for the endpoint in the given line.
    """
    for example in endpoint_examples:
        if example in line:
            print(f"Decorator found: {example} in line: {line}")
            return example
    return None
    

def find_flask_endpoints(flask_endpoint_examples, repo_path):
    """
    Find all API endpoints in the codebase using the examples provided by the user.
    """
    endpoint_patterns = [re.escape(example) for example in flask_endpoint_examples]

    # Initialize a list to store identified endpoints
    identified_endpoints = []

    # Use regular expressions to search for patterns in code files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_number, line in enumerate(lines, 1):
                        for pattern in endpoint_patterns:
                            if re.search(pattern, line):
                                function_name = extract_info_for_flask(lines, line_number, flask_endpoint_examples)
                                if function_name:
                                    identified_endpoints.append((file_path, line.strip(), function_name))
    return identified_endpoints

def find_express_endpoints(express_endpoint_examples, repo_path):
    """
    Find all API endpoints in the codebase using the examples provided by the user.
    """
    endpoint_patterns = [re.escape(example) for example in express_endpoint_examples]  

    # Initialize a list to store identified endpoints
    identified_endpoints = []

    # Use regular expressions to search for patterns in code files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(("js", "ts")):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line_number, line in enumerate(lines, 1):
                        for pattern in endpoint_patterns:
                            if re.search(pattern, line):
                                function_name = extract_info_for_express(lines, line_number, express_endpoint_examples)
                                if function_name:
                                    identified_endpoints.append((file_path, line.strip(), function_name))
    return identified_endpoints

def extract_info_for_flask(lines, line_number, endpoint_examples):
    """
        Extract the function name associated with a Flask endpoint, handling imported functions.
    """
    # Get the line containing the endpoint definition
    endpoint_line = lines[line_number - 1]
    print(endpoint_line)

    # Dynamically find the decorator used for the endpoint
    decorator = get_decorator_used(endpoint_line, endpoint_examples)

    if decorator:
        # Extract function name from the line
        function_name_match = re.search(r'def (\w+)\(', endpoint_line)
        if function_name_match:
            return function_name_match.group(1)

        # Check if the function is imported and then extract its name
        import_statement_match = re.search(r'from (\w+) import', endpoint_line)
        if import_statement_match:
            imported_module = import_statement_match.group(1)
            imported_function_match = re.search(r'(\w+)\(', endpoint_line)
            if imported_function_match:
                return f"{imported_module}.{imported_function_match.group(1)}"

    return None

def extract_info_for_express(lines, line_number, endpoint_examples):
    """
    Extract the function name associated with an Express endpoint.
    """
    # Get the line containing the endpoint definition
    endpoint_line = lines[line_number - 1]

    # Dynamically find the decorator used for the endpoint
    decorator = get_decorator_used(endpoint_line, endpoint_examples)

    if decorator:
        # Extract function name from the line
        function_name_match = re.search(r'\.(\w+)\(', endpoint_line)
        if function_name_match:
            return function_name_match.group(1)

        # Handle inline function definitions
        inline_function_match = re.search(r'\.(\w+)\(', endpoint_line)
        if inline_function_match:
            return inline_function_match.group(1)

        # Handle imported functions considering both es6 and commonjs
        import_statement_match = re.search(r'import (\w+) from', endpoint_line)
        if import_statement_match:
            imported_function_match = re.search(r'(\w+)\(', endpoint_line)
            if imported_function_match:
                return imported_function_match.group(1)
            
        require_statement_match = re.search(r'const (\w+) = require', endpoint_line)
        if require_statement_match:
            imported_function_match = re.search(r'(\w+)\(', endpoint_line)
            if imported_function_match:
                return imported_function_match.group(1)

    return None

