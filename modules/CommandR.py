"""
参考サイト
https://corkborg.github.io/wd14-tagger-standalone/
"""

# import time
import random
import cohere
from modules.Settings import Settings

chara = ["aaa", "bbb", "ccc", "ddd"]


class CommandRPlus:
    def __init__(self):

        self.co = cohere.ClientV2(api_key=Settings.llm_api_key)  # V2クライアントを使用
        self.chara_length = len(Settings.characters)
        self.last_selected = 0

    """
    キャラクターをランダムに選出
    """
    def get_random_character(self):
        # 利用可能なインデックスのリストを作成（前回のインデックスを除外）
        available_index = [i for i in range(self.chara_length) if i != self.last_selected]
        # ランダムに選択
        selected_index = random.choice(available_index)
        self.last_selected = selected_index

        return Settings.characters[selected_index]

    """
    画像タグを渡してコメントを受け取る
    """
    def get_comment(self, tags_str):
        # ランダムにキャラクターを選出し、プロンプトと合体する
        prompt = f"{Settings.prompt}{self.get_random_character()}"

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