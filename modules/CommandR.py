"""
参考サイト
https://corkborg.github.io/wd14-tagger-standalone/
"""

import cohere
from loguru import logger
from modules.Settings import Settings
from modules.Message import Message
from modules.utils import debug_print


class CommandRPlus:
    def __init__(self):
        self.co = cohere.ClientV2(api_key=Settings.llm_api_key)  # V2クライアントを使用


    """
    画像タグを渡してコメントを受け取る
    """
    def get_comment(self, prompt, tags_str):
        logger.debug(prompt)

        try:
            rag = self.co.chat(
                model="command-r-plus",
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": tags_str
                    }
                ]
            )
            
            # コメント文字数チェック
            if len(rag.message.content[0].text) > Settings.max_comment_length:
                return Message.msg.LLM_COMMENT_ERROR
            else:
                return rag.message.content[0].text
            
        except cohere.error.CohereError as e:
            # Cohereの特定のエラー
            error_message = f"Cohereのエラーが発生しました: {str(e)}"
            logger.error(error_message)  # ログ用
            return Message.msg.LLM_COMMENT_ERROR
            
        except Exception as e:
            # その他の予期せぬエラー
            error_message = f"予期せぬエラーが発生しました: {str(e)}"
            logger.error(error_message)  # ログ用
            return Message.msg.LLM_COMMENT_ERROR

