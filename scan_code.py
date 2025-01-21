import os
import sys
import git  # We will use GitPython to clone the repo
import openai
import shutil

# Get the API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # No hardcoded API key here


def scan_code(file_content):
    """Scan the code for issues using OpenAI."""
    # Modify prompt for better detection of issues in React code
    response = openai.Completion.create(
    engine="gpt-3.5-turbo",  # Updated model
    prompt=f"Analyze the following React code for syntax errors, incorrect imports, or potential improvements:\n\n{file_content}",
    max_tokens=500,  # Increase token limit to allow more detailed analysis
    temperature=0.1  # Make the model more deterministic
)

    
    # Log the raw response for debugging
    print("OpenAI Response:", response.choices[0].text.strip())  # Debugging line
    
    return response.choices[0].text.strip()

def scan_repository(repo_url):
    """Clone the repository and scan all files in the repository path."""
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(os.getcwd(), repo_name)

    # Clone the repository to the current working directory
    if not os.path.exists(repo_path):
        print(f"Cloning the repository {repo_url}...")
        git.Repo.clone_from(repo_url, repo_path)
    else:
        print(f"Repository already exists at {repo_path}")

    issues = []
    # Walk through the repository and scan relevant files
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.py', '.js', '.jsx')):  # Adjust extensions as needed
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:  # Ensure proper encoding
                    content = f.read()
                    result = scan_code(content)
                    if result:  # If there are any suggestions or issues found
                        issues.append((file_path, result))

    # Clean up by deleting the cloned repo (optional)
    shutil.rmtree(repo_path)
    
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scan_code.py <repo_url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    found_issues = scan_repository(repo_url)
    
    if found_issues:
        print("Issues found:")
        for file_path, issue in found_issues:
            print(f"File: {file_path}\nIssue: {issue}\n")
    else:
        print("No issues detected.")
