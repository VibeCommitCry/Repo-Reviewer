from enum import Enum


class ChunkTypeEnum(Enum):
    DOC = "doc"
    CODE = "code"
    OTHER = "other"
    
    
class SupportedLanguageEnum(Enum):
    PYTHON = ".py"
