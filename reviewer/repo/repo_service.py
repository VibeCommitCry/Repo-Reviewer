import re
import subprocess
import hashlib
from pathlib import Path
from reviewer.models.repo import RepoFile
from reviewer.models.enums import valid_language

REPO_URL = "https://github.com/"
CACHE_DIR = Path(__file__).resolve().parents[2] / "repos"

# owner/repo: letters, digits, '-', '_' and '.', exactly one slash
SLUG_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class RepoNotFoundError(Exception):
    """Raised when a repo can't be cloned or fetched."""


class RepoService:

    def _git(self, repo_path: Path, *args: str) -> str:
        """Run a git command inside repo_path and return its output."""
        result = subprocess.run(
            ["git", "-C", str(repo_path), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout

    def ensure_repo(self, slug: str) -> Path:
        """Clone the repo into the cache, or fetch it if it is already there."""
        if not SLUG_PATTERN.match(slug) or ".." in slug:
            raise ValueError(f"Invalid repo slug: {slug!r}, expected 'owner/repo'")

        folder = CACHE_DIR / slug.replace("/", "__")
        try:
            if (folder / ".git").is_dir():
                self._git(folder, "fetch", "--prune", "origin")
            else:
                folder.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(
                    ["git", "clone", f"{REPO_URL}{slug}.git", str(folder)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            return folder
        except subprocess.CalledProcessError as e:
            raise RepoNotFoundError(
                f"Could not clone '{slug}'. Check the name, or your access if it is private.\n"
                f"git said: {e.stderr.strip()}"
            ) from e

    def checkout(self, folder: Path, ref: str) -> None:
        """Point the working files at a branch (e.g. 'origin/main') or a PR."""
        self._git(folder, "checkout", "--detach", "--force", ref)

    def checkout_pr(self, folder: Path, pr_number: int) -> None:
        """Fetch a pull request's latest commits and check them out."""
        local_ref = f"pr-{pr_number}"
        self._git(folder, "fetch", "origin", f"+pull/{pr_number}/head:{local_ref}")
        self.checkout(folder, local_ref)

    def get_repo_files(self, folder: Path) -> list[RepoFile]:
        repo_files = []
        for path in self._git(folder, "ls-files").splitlines():
            repo_file = self._load_file(folder=folder, path=path)
            if repo_file is not None:
                repo_files.append(repo_file)
        return repo_files

    def _load_file(self, folder: Path, path: str) -> RepoFile | None:
        full_path = folder / path
        language = valid_language(full_path.suffix.lower())
        if language is None:  
            return None       

        try:
            content = full_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None  

        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return RepoFile(content=content, path=path, hash=file_hash, language=language)