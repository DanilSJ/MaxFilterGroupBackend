from pydantic import BaseModel, ConfigDict


class GroupSchema(BaseModel):
    id: int
    name: str
    group_id: int
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None
    message_delete_text: str = None
    bad_words_text: str = None
    stop_word_text: str = None

    pinned: bool = None

    model_config = ConfigDict(from_attributes=True)


class CreateGroupSchema(BaseModel):
    name: str
    group_id: int
    bad_words: bool
    repost: bool
    stop_word: bool
    link: bool
    message_delete: bool
    message_delete_text: str = None
    bad_words_text: str
    stop_word_text: str

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
    message_delete_text: str = None
    bad_words_text: str = None
    stop_word_text: str = None
    pinned: bool = None

    model_config = ConfigDict(from_attributes=True)