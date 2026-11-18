from reviewer.models.enums import SupportedLanguageEnum
from dataclasses import dataclass

@dataclass
class RepoFile:
    content: str
    path: str
    hash: str
    language: SupportedLanguageEnum

@dataclass
class FileChange:
    new: list[RepoFile]
    change: list[RepoFile]
    deleted: list[str]
