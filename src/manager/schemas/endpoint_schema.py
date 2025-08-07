# from enum import Enum

# from pydantic_settings import BaseSettings, SettingsConfigDict


# class EndpointSchema(BaseSettings):
#     model_config = SettingsConfigDict(env_prefix="ENDPOINT__")

#     # Endpoint prefixes
#     PREFIX_TAGS: str
#     PREFIX_SUBJECTS: str
#     PREFIX_PRIMARY_SUBJECT: str
#     PREFIX_SECONDARY_SUBJECT: str
#     PREFIX_ORGANIZATION: str

#     # Endpoint tags
#     TAGS_TAGS: list[str | Enum] | None
#     TAGS_SUBJECTS: list[str | Enum] | None
#     TAGS_PRIMARY_SUBJECT: list[str | Enum] | None
#     TAGS_SECONDARY_SUBJECT: list[str | Enum] | None
#     TAGS_ORGANIZATION: list[str | Enum] | None
