from pydantic import BaseModel, ConfigDict


class GridSchema(BaseModel):
    id: int
    name: str
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None

    bad_words_text: str = None
    stop_word_text: str = None

    pinned: bool = None

    model_config = ConfigDict(from_attributes=True)


class CreateGridSchema(BaseModel):
    name: str
    bad_words: bool
    repost: bool
    stop_word: bool
    link: bool
    message_delete: bool

    bad_words_text: str
    stop_word_text: str

    pinned: bool

    model_config = ConfigDict(from_attributes=True)


class UpdateGridSchemaPartial(BaseModel):
    name: str = None
    bad_words: bool = None
    repost: bool = None
    stop_word: bool = None
    link: bool = None
    message_delete: bool = None
    bad_words_text: str = None
    stop_word_text: str = None
    pinned: bool = None

    model_config = ConfigDict(from_attributes=True)