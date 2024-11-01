from dataclasses import dataclass
from typing import ClassVar
from pathlib import Path
import tomli
from loguru import logger
from modules.Settings import Settings

@dataclass
class MessageData:
    LLM_COMMENT_ERROR: str
    
    DISCORD_CHARA_DEFAULT: str
    DISCORD_CHARA_LIST: str
    DISCORD_CHARA_RANDOM: str
    DISCORD_CHARA_SET: str
    DISCORD_CHARA_NOT_EXISTS: str

    DISCORD_NOT_ALLOWED_CMD: str
    DISCORD_ATTACH_NORMAL: str
    DISCORD_ATTACH_MANY: str
    DISCORD_ATTACH_NOT_IMAGE: str


class Message:
    msg: ClassVar[MessageData]

    @classmethod
    def init(cls):
        try:
            with open(Settings.message_path, "rb") as f:
                data = tomli.load(f)
                cls.msg = MessageData(**data)
        except Exception as e:
            raise logger.error(f"メッセージの初期化に失敗: {e}")


    @classmethod
    def get(cls, message_id: str, **kwargs) -> str:
        """
        メッセージを取得して必要に応じて変数を置換
        Args:
            message_id: メッセージID
            **kwargs: 置換する変数
        """
        try:
            text = getattr(cls.msg, message_id)
            if kwargs:
                try:
                    return text.format(**kwargs)
                except KeyError as e:
                    raise logger.error(f"メッセージの置換に必要な変数がありません: {e}")
                except ValueError as e:
                    raise logger.error(f"メッセージの置換に失敗: {e}")
            return text
        except AttributeError:
            raise logger.error(f"メッセージID '{message_id}' が存在しません")
        
