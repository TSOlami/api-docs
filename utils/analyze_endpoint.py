import re
import os

def get_endpoint_examples():
	"""
	Ask the user to provide examples of how their API endpoints are defined in the codebase.
	"""

	print("Please provide examples of how your API endpoints are defined.")
	print("For example, you can provide lines of code that define an endpoint using decorators like @app.route, @server.route, etc for python and router.get, app.post, etc for node (express).")
	
	# initialize list of examples
	endpoint_examples = []

	# get examples from user
	while True:
		example = input("Enter an example and press enter. Enter 'done' when you are finished: ").strip()
		if example == 'done':
			break
		endpoint_examples.append(example)

	print(f"{len(endpoint_examples)} examples provided.")
	return endpoint_examples

def get_decorator_used(line, endpoint_examples):
    """
    Dynamically find the decorator used for the endpoint in the given line.
    """
    for example in endpoint_examples:
        if example in line:
            return example
    return None

def find_endpoints(examples, repo_path):
    """
    Find all API endpoints in the codebase using the examples provided by the user.
    """
    endpoint_patterns = [re.escape(example) for example in examples]

    # Initialize a list to store identified endpoints
    identified_endpoints = []

    # Use regular expressions to search for patterns in code files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                    # Search for endpoint patterns in the file content
                    for pattern in endpoint_patterns:
                        matches = re.finditer(pattern, file_content)
                        for match in matches:
                            identified_endpoints.append((file_path, match.group()))

    return identified_endpoints

def extract_info_for_flask(lines, line_number, endpoint_examples):
    """
        Extract the function name associated with a Flask endpoint, handling imported functions.
    """
    # Get the line containing the endpoint definition
    endpoint_line = lines[line_number - 1]

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

def extract_http_method(lines, line_number, endpoint_examples):
    """
    Extract the HTTP method associated with an endpoint.
    Implement logic based on codebase conventions and user-provided examples.
    """
    http_methods = ['GET', 'POST', 'PUT', 'DELETE']

    # Get the line containing the endpoint definition
    endpoint_line = lines[line_number - 1]

    # Dynamically find the decorator used for the endpoint
    decorator = get_decorator_used(endpoint_line, endpoint_examples)

    if decorator:
        # Use decorator information to infer HTTP method
        if 'route' in decorator:
            for method in http_methods:
                if method.lower() in decorator.lower():
                    return method

    # Look for lines containing HTTP methods near the endpoint definition
    for i in range(max(0, line_number-3), min(len(lines), line_number+3)):
        for method in http_methods:
            if method in lines[i]:
                return method

    return None
