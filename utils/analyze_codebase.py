import os

def analyze_repo(repo_path):
    """
    Analyzes the repository and returns basic information.
    """
    try:
        # Count the number of files and directories
        num_files = 0
        num_dirs = 0
        for root, dirs, files in os.walk(repo_path):
            num_dirs += len(dirs)
            num_files += len(files)

        # Count the total lines of code
        num_lines = 0
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        num_lines += len(f.readlines())

        # List the files in the repository (excluding .git directory)
        file_list = []
        for root, dirs, files in os.walk(repo_path):
            if '.git' in dirs:
                dirs.remove('.git')  # Exclude .git directory
            for file in files:
                if not file.startswith('.git'):
                    file_list.append(os.path.relpath(os.path.join(root, file), repo_path))

        analysis_result = f"Repository Analysis:\n" \
                          f"Number of files: {num_files}\n" \
                          f"Number of directories: {num_dirs}\n" \
                          f"Total lines of code: {num_lines}\n\n" \
                          f"List of files:\n{', '.join(file_list)}"

        return analysis_result

    except Exception as e:
        return f"Error analyzing repository: {e}"
