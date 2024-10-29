"""
参考サイト
https://corkborg.github.io/wd14-tagger-standalone/
"""

from pathlib import Path
import time
import cohere
from modules.Settings import Settings

class CommandRPlus:
    def __init__(self):

        self.prompt = Path(Settings.prompt_path).read_text(encoding='utf-8')
        self.co = cohere.ClientV2(api_key=Settings.llm_api_key)  # V2クライアントを使用

    """
    画像タグを渡してコメントを受け取る
    """
    def get_comment(self, tags_str):

        rag = self.co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "system",
                    "content": self.prompt
                },
                {
                    "role": "user",
                    "content": tags_str
                }
            ]
        )
        return rag.message.content[0].text
