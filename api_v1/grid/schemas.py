from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from api_v1.group.schemas import GroupSchema


class GridSchema(BaseModel):
    id: int
    name: str
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None
    message_delete_text: Optional[str] = None

    bad_words_text: str = None
    stop_word_text: str = None

    pinned: bool = None
    groups: List[GroupSchema] = None

    message_bad_text: Optional[str] = None
    message_stop_word_text: Optional[str] = None
    message_link_text: Optional[str] = None
    message_repost_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CreateGridSchema(BaseModel):
    name: str
    bad_words: bool
    repost: bool
    stop_word: bool
    link: bool
    message_delete: bool
    message_delete_text: Optional[str] = None
    bad_words_text: str
    stop_word_text: str
    pinned: bool
    group_ids: List[int] = None

    message_bad_text: Optional[str] = None
    message_stop_word_text: Optional[str] = None
    message_link_text: Optional[str] = None
    message_repost_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UpdateGridSchemaPartial(BaseModel):
    name: str = None
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None
    message_delete_text: Optional[str] = None
    bad_words_text: str = None
    stop_word_text: str = None
    pinned: bool = None
    group_ids: List[int] = None

    message_bad_text: Optional[str] = None
    message_stop_word_text: Optional[str] = None
    message_link_text: Optional[str] = None
    message_repost_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)