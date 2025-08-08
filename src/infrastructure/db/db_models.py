from datetime import datetime, timezone
from uuid import uuid4

import sqlalchemy as sa
import sqlalchemy.orm as so

from src.common import types
from src.infrastructure.db.meta_data import BaseModel


class File(BaseModel):
    __tablename__ = "files"
    name: so.Mapped[str] = so.mapped_column(sa.Text, unique=True)
    file_name: so.Mapped[str] = so.mapped_column(sa.String(250))
    type: so.Mapped[str] = so.mapped_column(sa.String(250))  # TODO: 1
    # TODO: 2 => Added user_id when JWT token added to system.
    size: so.Mapped[int]
    extension: so.Mapped[str]
    id: so.Mapped[types.FileId] = so.mapped_column(
        primary_key=True, default=lambda: uuid4()
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
