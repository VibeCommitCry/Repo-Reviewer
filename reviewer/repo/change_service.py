from reviewer.models.repo import FileChange, RepoFile


class ChangeService:

    def compare(
        self, repo_files: list[RepoFile], indexed_hashes: dict[str, str]
    ) -> FileChange:
        current = {f.path: f for f in repo_files}
        
        common_keys = set(current) & indexed_hashes.keys()
        
        # Find list items NOT in dict keys (difference)
        missing_keys = set(current) - indexed_hashes.keys()  # set()

        # Check exact match (ignoring order)
        is_exact_match = set(current) == indexed_hashes.keys()  # False

        # Check exact match (preserving order)
        is_ordered_match = current == list(indexed_hashes.keys())  # False

        print(f"common_keys: {common_keys}\n")
        print(f"missing_keys: {missing_keys}\n")
        print(f"is_exact_match: {is_exact_match}\n")
        print(f"is_ordered_match: {is_ordered_match}\n")
