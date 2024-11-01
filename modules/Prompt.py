"""
character の TOMLは下記のような書式
"""

# [[characters]]
# name = "美優"
# profile = """
#   - 名前：美優
#   - 性別：女
#   - 年齢：14歳
#   - 一人称：美優
#   - 性的なものに興味津々でＨなイラストが大好き
#   - 少女らしく「きゃー！」とか「かっわいーい！」など感情をストレートに表現する
#   - 少女自身はSEX未経験なので性的なものに憧れがある
#   - 絵を見るとインスピレーションが湧いて歌い出す
#   - 和歌（五七五という文字数制限の歌）を詠む時もある
# """



import random
from pathlib import Path
import tomli
from modules.Settings import Settings

class Prompt:
    prompt = ""
    characters = []
    last_selected = 0

    @classmethod
    def init(cls):
        # 基本プロンプト
        cls.prompt = Path(Settings.prompt_path).read_text(encoding='utf-8')

        # キャラクター一覧
        with open(Settings.character_path, "rb") as f:
            data = tomli.load(f)
            cls.characters = data["characters"]

    """
    キャラリスト一覧を取得
    """
    @classmethod
    def get_chara_list(cls):
        # 全キャラクターの名前を取得してリスト化
        names = []
        for chara in cls.characters:
            if isinstance(chara, dict) and "name" in chara:
                names.append(chara["name"])
            
        # 箇条書きのテキストを作成
        text = "\n".join([f"* {name}" for name in names])
        
        return text        

    """
    指定したキャラクターが存在するか確認
    """
    @classmethod
    def is_exists_chara(cls, name):
        for chara in cls.characters:
            if isinstance(chara, dict) and "name" in chara:
                if chara["name"] == name:
                    return True
        return False

    """
    プロンプトを取得
    """
    @classmethod
    def get_prompt(cls, chara = "random"):
        profile = cls.get_random_chara()["profile"]

        return f"{cls.prompt}\n{profile}"

    """
    キャラクターをランダムに選出
    """
    @classmethod
    def get_random_chara(cls):
        chara_length = len(cls.characters)

        # 利用可能なインデックスのリストを作成（前回のインデックスを除外）
        available_index = [i for i in range(chara_length) if i != cls.last_selected]
        # ランダムに選択
        selected_index = random.choice(available_index)
        cls.last_selected = selected_index

        return cls.characters[selected_index]
    