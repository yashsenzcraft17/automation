import os
import git
from github import Github

# Function to retrieve the GitHub token from an environment variable
def get_github_token():
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GitHub token not found in environment variables.")
    return github_token

def commit_and_push(branch_name, commit_message):
    repo = git.Repo('.')

    # Check if there are changes to commit
    if repo.is_dirty(untracked_files=True):
        # Add all changes (including modifications and additions)
        repo.git.add('--all')

        # Commit changes
        repo.git.commit('-m', commit_message)
        print(f"Committed changes in '{branch_name}' with message: {commit_message}")

        # Push changes to the remote repository
        try:
            repo.git.push('origin', branch_name)
            print(f"Pushed changes to '{branch_name}'")
        except git.GitCommandError as e:
            print(f"Error pushing changes to '{branch_name}': {e}")
    else:
        print(f"No changes to commit in '{branch_name}'")

def get_existing_pull_request(repo, src_branch, dest_branch):
    try:
        pull_requests = repo.get_pulls(state='open', head=f'yashsenzcraft17:{src_branch}', base=f'yashsenzcraft17:{dest_branch}')
        return pull_requests[0] if pull_requests else None
    except Exception as e:
        print(f"Error retrieving existing pull request: {e}")
        return None

def close_pull_request(pull_request):
    try:
        pull_request.edit(state='closed')
        print(f"Closed existing pull request: {pull_request.html_url}")
    except Exception as e:
        print(f"Error closing pull request: {e}")

def merge_pull_request(pull_request):
    try:
        pull_request.merge()
        print(f"Pull request merged successfully")
    except Exception as e:
        print(f"Error merging pull request: {e}")

def push_and_merge_pull_request(src_branch, dest_branch, title, body):
    repo = git.Repo('.')

    # Commit and push changes in the source branch
    commit_message = "Your commit message for testing changes"
    commit_and_push(src_branch, commit_message)

    # Push changes to the remote testing branch
    try:
        repo.git.push('origin', src_branch)
        print(f"Pushed changes to '{src_branch}'")
    except git.GitCommandError as e:
        print(f"Error pushing changes to '{src_branch}': {e}")

    # Create a pull request or get the existing one from the remote "testing" to the remote "staging"
    github_token = get_github_token()
    g = Github(github_token)
    github_repo = g.get_repo('yashsenzcraft17/automation')  # Replace with your actual repository information
    existing_pull_request = get_existing_pull_request(github_repo, src_branch, dest_branch)

    if existing_pull_request:
        print(f"Using existing pull request: {existing_pull_request.html_url}")
        # Optionally close the existing pull request
        close_pull_request(existing_pull_request)
    else:
        # Create a new pull request
        pull_request = github_repo.create_pull(
            title=title,
            body=body,
            base=dest_branch,
            head=src_branch,
            draft=False
        )
        print(f"Pull request created: {pull_request.html_url}")

    # Print the status to check the changes in the local testing branch
    print(repo.git.status())

    # Merge the pull request
    merge_pull_request(pull_request)

    # Push changes to the remote testing branch (optional, depending on your workflow)
    try:
        repo.git.push('origin', src_branch)
        print(f"Pushed changes to '{src_branch}'")
    except git.GitCommandError as e:
        print(f"Error pushing changes to '{src_branch}': {e}")

if __name__ == "__main__":
    # Replace 'testing', 'staging' with your branch names
    push_and_merge_pull_request('testing', 'staging', 'testing', 'testing')
