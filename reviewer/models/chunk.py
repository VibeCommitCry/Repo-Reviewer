from dataclasses import dataclass
from reviewer.models.enums import SupportedLanguageEnum, ChunkTypeEnum


@dataclass
class Chunk:
    id: str
    hash: str
    file: str
    content: str
    start: int
    end: int
    chunktype: ChunkTypeEnum
    language: SupportedLanguageEnum


class SearchResult:
    pass


class ContextResult:
    pass
