from enum import Enum


class ChunkTypeEnum(Enum):
    DOC = "doc"
    CODE = "code"
    OTHER = "other"
    
    
class SupportedLanguageEnum(Enum):
    PYTHON = ".py"
    MARKDOWN = ".md"



def valid_language(extension: str) -> SupportedLanguageEnum | None:
    try:
        return SupportedLanguageEnum(extension)
    except ValueError:
        return None