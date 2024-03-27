import os, stat
import shutil

from utils import analyze_codebase, analyze_endpoint


def remove_readonly(func, path, _):
	"""
	Removes the read-only attribute from a file or directory.
	"""
	os.chmod(path, stat.S_IWRITE)
	func(path)

def main():
	"""
	Clones a Github repo and analyzes it to generate documentation for the API endpoints.
	"""

	# Get the Github repo URL from the user
	repo_url = input("Enter the Github repo URL: ")

	# Get the repo name from the URL
	repo_name = repo_url.split("/")[-1].replace(".git", "")
	print(f"Repo name: {repo_name}")
	clone_directory = "repos"
	repo_path = os.path.join(clone_directory, repo_name)

	try:
		# Create the directory to clone the repo into
		if not os.path.exists(clone_directory):
			os.mkdir(clone_directory)
			print(f"Created directory {clone_directory}")
		
		# Clone the repo into the directory
		os.system(f"git clone {repo_url} {repo_path}")
		print(f"Cloned repo into {repo_path}")

		# Analyze the entire repository
		repo_analysis, uses_flask, uses_express = analyze_codebase.analyze_repo(repo_path)

		# Print the analysis result
		print(repo_analysis)
		
		# If at least one of the frameworks is used, proceed with endpoint identification
		if uses_flask:
			print("Flask framework usage identified. Proceeding with endpoint identification.")

			# Get examples of API endpoints from the user
			flask_endpoint_examples = analyze_endpoint.get_flask_endpoint_examples()
			
			# Find all API endpoints in the codebase using the examples provided by the user
			identified_flask_endpoints = analyze_endpoint.find_flask_endpoints(flask_endpoint_examples, repo_path)
			print("Found endpoints: ", identified_flask_endpoints)

		if uses_express:
			print("Express framework usage identified. Proceeding with endpoint identification.")

			# Get examples of API endpoints from the user
			express_endpoint_examples = analyze_endpoint.get_express_endpoint_examples()

			# Find all API endpoints in the codebase using the examples provided by the user
			identified_express_endpoints = analyze_endpoint.find_express_endpoints(express_endpoint_examples, repo_path)
			print("Found endpoints: ", identified_express_endpoints)

		else:
			print("Unable to identify the framework used. Cannot continue with documentation generation.")
			return

	except Exception as e:
		print(f"Error: {e}")

	finally:
		try:
			# Delete the cloned repo
			print(f"Deleting repo {repo_path}")
			shutil.rmtree(repo_path, onerror=remove_readonly)
			print(f"Deleted repo {repo_path}")

			print("Done")
		except Exception as e:
			# If the repo was not cloned successfully, the directory will not exist
			print(f"Error: {e}")


if __name__ == "__main__":
	main()