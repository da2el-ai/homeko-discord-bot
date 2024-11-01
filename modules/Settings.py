import os
from dotenv import load_dotenv
import yaml



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
    prompt_path = str(os.getenv('PROMPT_PATH', 'prompt.md'))
    character_path = str(os.getenv('CHARACTER_PATH', 'character.toml'))
    # コメント最大数
    max_comment_length = int(os.getenv('MAX_COMMENT_LENGTH', 400))

    # メッセージファイル
    message_path = str(os.getenv('MESSAGE_PATH', 'message.toml'))
