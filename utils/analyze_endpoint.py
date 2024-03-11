import re

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

def find_endpoints_in_code(examples, repo_path):
	"""
	Find all API endpoints in the codebase using the examples provided by the user.
	"""
	pass