from enum import Enum


class MessageTypes(Enum):
    TYPE_TEXT = 0
    TYPE_PHOTO = 1
    TYPE_STICKER = 2
    TYPE_GIF = 3
    TYPE_VOICE = 4
    TYPE_AUDIO = 4
    TYPE_VIDEO = 6
    TYPE_FILE = 7
