import git

def commit_and_push(branch_name, commit_message):
    repo = git.Repo('.')

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

def push_and_pull(src_branch, dest_branch):
    repo = git.Repo('.')

    # Commit and push changes in the source branch
    commit_message = "Your commit message for dev changes"
    commit_and_push(src_branch, commit_message)

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

    # Checkout the source branch
    repo.git.checkout(src_branch)
    print(f"Checked out source branch '{src_branch}'")

    # Pull the latest changes from the source branch
    try:
        repo.git.pull('origin', src_branch)
        print(f"Pulled latest changes from '{src_branch}'")
    except git.GitCommandError as e:
        print(f"Error pulling changes from '{src_branch}': {e}")

    # Merge changes from source to destination
    repo.git.merge(src_branch)
    print(f"Merged changes from '{src_branch}' to '{dest_branch}'")

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
    # Replace 'dev', 'testing', 'main' with your branch names
    push_and_pull('dev', 'staging')