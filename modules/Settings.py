import os
from dotenv import load_dotenv

"""
設定 class
"""
class Settings:
    load_dotenv()

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

    # CommandR+ に渡す指示ファイル
    prompt_path = str(os.getenv('PROMPT_PATH', 'prompt.md'))
