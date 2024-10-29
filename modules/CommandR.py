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
        try:
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
            
        except cohere.error.CohereError as e:
            # Cohereの特定のエラー
            error_message = f"Cohereのエラーが発生しました: {str(e)}"
            print(error_message)  # ログ用
            return "ごめんね、コメントの生成に失敗しちゃった... 後でもう一度試してみてね！"
            
        except Exception as e:
            # その他の予期せぬエラー
            error_message = f"予期せぬエラーが発生しました: {str(e)}"
            print(error_message)  # ログ用
            return "ごめんね、なにか問題が起きちゃった... 後でもう一度試してみてね！"