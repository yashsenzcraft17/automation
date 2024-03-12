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

def create_and_checkout_branch(branch_name):
    repo = git.Repo('.')

    # Fetch branch from remote
    repo.git.fetch('origin', branch_name)

    # Create and checkout the branch
    try:
        repo.git.checkout('-b', branch_name, f'origin/{branch_name}')
        print(f"Checked out and created branch '{branch_name}'")
    except git.GitCommandError as e:
        print(f"Error creating and checking out branch '{branch_name}': {e}")

def create_pull_request(repo, src_branch, dest_branch, title, body):
    try:
        base = repo.get_branch(dest_branch)
        head = repo.get_branch(src_branch)
        pull_request = repo.create_pull(
            title=title,
            body=body,
            base=base.name,
            head=head.name,
            draft=False
        )
        print(f"Pull request created: {pull_request.html_url}")
        return pull_request
    except Exception as e:
        print(f"Error creating pull request: {e}")
        return None

def merge_pull_request(pull_request):
    try:
        pull_request.merge()
        print(f"Pull request merged successfully")
    except Exception as e:
        print(f"Error merging pull request: {e}")

def push_and_merge_pull_request(src_branch, dest_branch, title, body):
    repo = git.Repo('.')

    # Ensure the destination branch exists locally
    if dest_branch not in repo.branches:
        create_and_checkout_branch(dest_branch)
    else:
        # Checkout the destination branch
        repo.git.checkout(dest_branch)
        print(f"Checked out existing branch '{dest_branch}'")

        # Pull the latest changes from the destination branch
        try:
            repo.git.pull('origin', dest_branch)
            print(f"Pulled latest changes from '{dest_branch}'")
        except git.GitCommandError as e:
            print(f"Error pulling changes from '{dest_branch}': {e}")

    # Commit and push changes in the source branch
    commit_message = "Your commit message for dev changes"
    commit_and_push(src_branch, commit_message)

    # Create a pull request
    github_token = get_github_token()
    g = Github(github_token)
    github_repo = g.get_repo('yashsenzcraft17/automation')  # Replace with your actual repository information
    pull_request = create_pull_request(github_repo, src_branch, dest_branch, title, body)

    if pull_request:
        # Merge the pull request
        merge_pull_request(pull_request)

    # Print the status to check the changes in the local staging branch
    print(repo.git.status())

    # Push changes to both source and destination branches
    try:
        repo.git.push('origin', src_branch)
        print(f"Pushed changes to '{src_branch}'")
        repo.git.push('origin', dest_branch)
        print(f"Pushed changes to '{dest_branch}'")
    except git.GitCommandError as e:
        print(f"Error pushing changes: {e}")

if __name__ == "__main__":
    # Replace 'dev', 'staging' with your branch names
    push_and_merge_pull_request('testing', 'staging', 'testing', 'testing')
