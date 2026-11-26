from reviewer.models.enums import SupportedLanguageEnum
from dataclasses import dataclass

@dataclass
class RepoFile:
    content: str
    path: str
    hash: str
    language: SupportedLanguageEnum
    
    def __repr__(self) -> str:
        return (
            f"RepoFile:\n"
            f"  content: {self.content}\n"
            f"  path: {self.path}\n"
            f"  hash: {self.hash}\n"
            f"  language: {self.language}\n"
            # f"  Content: {self.content}\n"
        )

@dataclass
class FileChange:
    new: list[RepoFile]
    changed: list[RepoFile]
    deleted: list[str]
