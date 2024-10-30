import os
from dotenv import load_dotenv
from pathlib import Path
import yaml


def load_character(yaml_file):
    try:
        with open(yaml_file, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

            if not isinstance(data["characters"], list):
                raise ValueError(f"配列になっていません: {str(data)}")
            
            return data["characters"]

    except FileNotFoundError:
        raise FileNotFoundError(f"ファイル '{yaml_file}' が見つかりません")
    except yaml.YAMLError as e:
        raise ValueError(f"YAMLの解析エラー: {str(e)}")

"""
設定 class
"""
class Settings:
    load_dotenv()

    # デバッグメッセージを表示するか
    debug = str(os.getenv('DEBUG', 'false')).lower() == 'true'

    # 画像保存フォルダ
    image_folder = str(os.getenv('IMAGE_FOLDER', 'images'))

    # コマンド接頭辞
    prefix = str(os.getenv('COMMAND_PREFIX', '!'))

    # Discord TOKEN
    discord_token = os.getenv('DISCORD_TOKEN')

    # 参加可能なチャンネル
    channel_ids_str = os.getenv('ALLOWED_CHANNELS', '')  # 存在しない場合は空文字を返す
    allowed_channels = [int(id) for id in channel_ids_str.split(',')] if channel_ids_str else []

    # CommandR+ の APIキー
    llm_api_key = os.getenv('LLM_API_KEY')

    # CommandR+ に渡すプロンプト
    prompt = Path(str(os.getenv('PROMPT_PATH', 'prompt.md'))).read_text(encoding='utf-8')
    characters = load_character(str(os.getenv('CHARACTER_PATH', 'character.yaml')))
    # コメント最大数
    max_comment_length = int(os.getenv('MAX_COMMENT_LENGTH', 400))

    # LLMコメントエラー
    msg_comment_error = str(os.getenv('MSG_COMMENT_ERROR'))
