import re
import os

def get_endpoint_examples():
	"""
	Ask the user to provide examples of how their API endpoints are defined in the codebase.
	"""

	print("Please provide examples of how your API endpoints are defined.")
	print("For example, you can provide lines of code that define an endpoint using decorators like @app.route, @server.route, @auth.route, @views.route, etc.")
	
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
