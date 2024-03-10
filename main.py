import os, stat
import shutil

from utils import analyze_codebase


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

		# Analyze the repo
		analysis_result = analyze_codebase.analyze_repo(repo_path)
		print(analysis_result)

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