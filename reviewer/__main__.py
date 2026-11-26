import sys

from reviewer.repo.repo_service import RepoNotFoundError, RepoService
from reviewer.repo.change_service import ChangeService

if __name__ == "__main__":

    try:
        repo_service = RepoService()
        change_service = ChangeService()
        slug = "VibeCommitCry/Repo-Reviewer"

        path = repo_service.ensure_repo(slug=slug)
        repo_service.checkout(path, "origin/main")
        print(f"path = {path}\n")

        files = repo_service.get_repo_files(folder=path)
        indexed_hashes = {
            'README.md': "abc",
            r"reviewer\__main__.py": "",
            r"reviewer\config.py": ""
        }       
         
        file_changes = change_service.compare(repo_files=files, indexed_hashes=indexed_hashes)

    except RepoNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
