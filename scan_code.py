import os
import sys  # Import sys module to use sys.argv
import openai

# Set the API key directly in the environment
os.environ["OPENAI_API_KEY"] = "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"

# Assign it to the OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def scan_code(file_content):
    """Scan the code for issues using OpenAI."""
    # Modify prompt for better detection of issues in React code
    response = openai.Completion.create(
        engine="text-davinci-003",  # Codex or GPT model
        prompt=f"Analyze the following React code for syntax errors, incorrect imports, or potential improvements:\n\n{file_content}",
        max_tokens=500,  # Increase token limit to allow more detailed analysis
        temperature=0.1  # Make the model more deterministic
    )
    
    # Log the raw response for debugging
    print("OpenAI Response:", response.choices[0].text.strip())  # Debugging line
    
    return response.choices[0].text.strip()

def scan_repository(repo_path):
    """Scan all files in the specified repository path."""
    issues = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.py', '.js', '.jsx')):  # Adjust extensions as needed
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:  # Ensure proper encoding
                    content = f.read()
                    result = scan_code(content)
                    if result:  # If there are any suggestions or issues found
                        issues.append((file_path, result))
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 scan_code.py <repo_path>")
        sys.exit(1)

    repo_path = sys.argv[1]
    found_issues = scan_repository(repo_path)
    
    if found_issues:
        print("Issues found:")
        for file_path, issue in found_issues:
            print(f"File: {file_path}\nIssue: {issue}\n")
    else:
        print("No issues detected.")
