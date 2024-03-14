import git

def pull_from_testing_and_push_to_staging(src_branch, dest_branch):
    repo = git.Repo('.')

    # Ensure that the provided branches are remote branches
    src_remote_branch = f"origin/{src_branch}"
    dest_remote_branch = f"origin/{dest_branch}"

    # Pull changes from testing remote branch to staging remote branch
    try:
        repo.git.fetch('origin', src_branch)  # Fetch changes from testing remote branch
        repo.git.push('origin', f"{src_branch}:{dest_branch}")  # Push changes from testing to staging
        print(f"Pulled changes from '{src_branch}' and pushed to '{dest_branch}'")
    except git.GitCommandError as e:
        print(f"Error pulling and pushing changes from '{src_branch}' to '{dest_branch}': {e}")

if __name__ == "__main__":
    # Replace 'testing', 'staging' with your branch names
    pull_from_testing_and_push_to_staging('testing', 'staging')
