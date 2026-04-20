from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from api_v1.user.schemas import UserSchema


class GridMiniSchema(BaseModel):
    id: int
    name: str
    block_users: List[UserSchema] = None
    model_config = ConfigDict(from_attributes=True)

class GroupSchema(BaseModel):
    id: int
    name: str
    group_id: int
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None
    message_delete_text: Optional[str] = None

    message_bad_text: Optional[str] = None
    message_stop_word_text: Optional[str] = None
    message_link_text: Optional[str] = None
    message_repost_text: Optional[str] = None

    bad_words_text: str = None
    stop_word_text: str = None

    pinned: bool = None

    position: Optional[int] = None

    grid: Optional[GridMiniSchema] = None

    model_config = ConfigDict(from_attributes=True)


class CreateGroupSchema(BaseModel):
    name: str
    group_id: int
    bad_words: bool
    repost: bool
    stop_word: bool
    link: bool
    message_delete: bool
    message_delete_text: Optional[str] = None
    bad_words_text: str
    stop_word_text: str

    message_bad_text: Optional[str] = None
    message_stop_word_text: Optional[str] = None
    message_link_text: Optional[str] = None
    message_repost_text: Optional[str] = None

    pinned: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateGroupSchemaPartial(BaseModel):
    name: str = None
    group_id: int = None
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None
    message_delete_text: Optional[str] = None
    bad_words_text: str = None
    stop_word_text: str = None
    pinned: bool = None

    message_bad_text: Optional[str] = None
    message_stop_word_text: Optional[str] = None
    message_link_text: Optional[str] = None
    message_repost_text: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)