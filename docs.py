import os
import git

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
            # Push to the remote tracking branch
            repo.git.push('origin', f"{branch_name}:refs/heads/{branch_name}")
            print(f"Pushed changes to '{branch_name}'")
        except git.GitCommandError as e:
            print(f"Error pushing changes to '{branch_name}': {e}")
    else:
        print(f"No changes to commit in '{branch_name}'")

def pull_from_testing_and_push_to_staging(src_branch, dest_branch):
    repo = git.Repo('.')

    # Ensure that the provided branches are remote branches
    src_remote_branch = f"origin/{src_branch}"
    dest_remote_branch = f"origin/{dest_branch}"

    # Change to the staging branch
    try:
        repo.git.checkout(dest_remote_branch)
        print(f"Changed to branch '{dest_remote_branch}'")
    except git.GitCommandError as e:
        print(f"Error changing to branch '{dest_remote_branch}': {e}")
        return

    # Pull changes from testing remote branch to local staging branch
    try:
        repo.git.pull('origin', src_branch)
        print(f"Pulled changes from '{src_branch}' to '{dest_branch}'")
    except git.GitCommandError as e:
        print(f"Error pulling changes from '{src_branch}' to '{dest_branch}': {e}")
        return

    # Push changes to the staging remote branch
    try:
        # Push to the remote tracking branch
        repo.git.push('origin', f"{dest_branch}:refs/heads/{dest_branch}")
        print(f"Pushed changes to '{dest_branch}'")
    except git.GitCommandError as e:
        print(f"Error pushing changes to '{dest_branch}': {e}")

if __name__ == "__main__":
    # Replace 'testing', 'staging' with your branch names
    commit_and_push('testing', 'Your commit message for testing changes')
    pull_from_testing_and_push_to_staging('testing', 'staging')
