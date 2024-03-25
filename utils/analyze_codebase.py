import os
import re

def analyze_repo(repo_path):
    """
    Analyzes the repository and returns basic information.
    """
    try:
        # Initialize counters
        num_files = 0
        num_dirs = 0
        num_lines = 0

        # Initialize flags	
        uses_flask = False
        uses_express = False

        # Walk through the repository and count files, directories, and lines of code
        for root, dirs, files in os.walk(repo_path):
            num_dirs += len(dirs)
            for file in files:
                num_files += 1
                file_path = os.path.join(root, file)
                # Check if the file is a Python or JavaScript file
                if file.endswith(".py"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f"Analyzing file: {file_path}")
                        num_lines += sum(1 for line in f)
                        f.seek(0)
                        file_content = f.read()
                        print(file_content)
                        flask_pattern_match = re.search(r'Flask\s*\(\s*__name__\s*\)', file_content)
                        if flask_pattern_match:
                            uses_flask = True

                elif file.endswith((".js", ".ts")):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f"Analyzing file: {file_path}")
                        num_lines += sum(1 for line in f)
                        f.seek(0)
                        file_content = f.read()
                        print(file_content)
                        express_pattern_match = re.search(r'express\.Router\s*\(\s*\)', file_content)
                        if express_pattern_match:
                            uses_express = True

        # Get a list of all files in the repository
        file_list = []
        for root, dirs, files in os.walk(repo_path):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                if not file.startswith('.git'):
                    file_list.append(os.path.relpath(os.path.join(root, file), repo_path))

        # Generate and return the analysis result
        analysis_result = f"Repository Analysis:\n" \
                          f"Number of files: {num_files}\n" \
                          f"Number of directories: {num_dirs}\n" \
                          f"Total lines of code: {num_lines}\n\n" \
                          f"List of files:\n{', '.join(file_list)}\n\n" \
                          f"Framework Usage:\nFlask: {uses_flask}\nExpress: {uses_express}"

        return analysis_result, uses_flask, uses_express

    except Exception as e:
        return f"Error analyzing repository: {e}"
