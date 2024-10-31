from pathlib import Path
from datetime import datetime 
import uuid
import discord
from .Settings import Settings


def debug_print(value):
    if Settings.debug:
        print(value)
        

"""
画像を保存
"""
async def save_image(attachment:discord.Attachment, folder:str):
    # フォルダを作る
    save_dir = Path(folder)
    save_dir.mkdir(exist_ok=True)

    # ファイル名を日付＋UUIDに
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_ext = Path(attachment.filename).suffix.lower()
    file_name = f"{timestamp}_{uuid.uuid4()}{file_ext}"
    file_path = save_dir / file_name

    # 画像保存
    try:
        await attachment.save(file_path)
        responce = (
            f"画像を受け取りました\n"
            f"ファイル名: {attachment.filename}\n"
        )
        return True, responce, file_path
    except Exception as e:
        responce = (
            f"画像の保存に失敗しました\n"
            f"エラー: {str(e)}"
        )
        return False, responce, file_path
    