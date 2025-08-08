from uuid import UUID
from typing import NewType
from enum import StrEnum

FileId = NewType("FileId", UUID)


class FileTypeEnum(StrEnum):
    ORGANIZATION_LOGO = "ORGANIZATION_LOGO"
    SUBJECT_LOGO = "SUBJECT_LOGO"
    INDICATOR_EXL = "INDICATOR_EXL"
