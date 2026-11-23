import sys

from reviewer.repo.repo_service import RepoNotFoundError, RepoService

if __name__ == "__main__":

    try:
        slug = "VibeCommitCry/Repo-Reviewer"
        path = RepoService().ensure_repo(slug=slug)
        print(f"path = {path}\n")
        
        RepoService().get_repo_files(folder=path)
    except RepoNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
