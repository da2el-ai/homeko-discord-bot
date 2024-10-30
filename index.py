from pathlib import Path
import os
import uuid
import asyncio
from datetime import datetime 
import discord
from discord.ext import commands
from modules.Settings import Settings
from modules.Tagger import Tagger
from modules.CommandR import CommandRPlus
from modules.utils import debug_print

# チェック関数をクラスの外に配置
def in_allowed_channel():
    async def predicate(ctx):
        return ctx.channel.id in Settings.allowed_channels
    return commands.check(predicate)


"""
Discord bot class
"""
class MyDiscordBot:
    def __init__(self):
        # Discordのインテント設定
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.setup_commands()
        self.setup_events()
        self.llm = CommandRPlus()


    """
    コマンド設定
    """
    def setup_commands(self):
        @self.bot.event
        async def on_ready():
            await self.on_ready()

        @self.bot.command()
        @in_allowed_channel()
        async def hoge(ctx):
            await self.cmd_hoge(ctx)

        @hoge.error
        async def hoge_error(ctx, error):
            if isinstance(error, commands.CheckFailure):
                await ctx.send('このコマンドはこのチャンネルでは使用出来ません')

    """
    イベント設定
    """
    def setup_events(self):
        @self.bot.event
        async def on_message(message):
            # botからのメッセージは無視
            if message.author.bot:
                return
            
            # 許可されたチャンネルか
            if message.channel.id not in Settings.allowed_channels:
                return
            
            # 添付ファイルがある場合
            if message.attachments:
                await self.handle_attachment(message)

            # この行は必須！コマンドの処理を行うため
            await self.bot.process_commands(message)

    """
    画像添付されていた
    """
    async def handle_attachment(self, message):
        # 画像ファイルの数をカウント
        image_attachments = [
            att for att in message.attachments 
            if any(att.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp'])
        ]

        # 画像が2つ以上の場合
        if len(image_attachments) > 1:
            await message.channel.send(f'{message.author.mention} たくさんのイラストをありがとう！最初の1枚だけ見させてもらうね☆', reference=message)
        elif image_attachments:
            await message.channel.send(f'{message.author.mention} イラストありがとっ！見させてもらうね☆', reference=message)
        else:
            await message.channel.send(f'{message.author.mention} これイラストじゃないよ？', reference=message)
            return

        # 最初の画像のみを処理
        await self.process_image(message, image_attachments[0])


    """
    画像処理
    """
    async def process_image(self, message, attachment):
        # 画像を保存
        success, responce, file_path = await self.save_image(attachment)

        # 画像保存失敗メッセージ
        if not success:
            await message.channel.send(responce)
            return

        # LLMからコメント取得
        asyncio.create_task(self.process_llm(message, file_path))

    """
    LLMからコメント取得
    """
    async def process_llm(self, message, file_path):
        try:
            # タグ取得
            tags = Tagger.get_tags(file_path)
            tags_str = ', '.join(tags.keys())
            debug_print(tags_str)

            # LLMからコメント取得
            comment = self.llm.get_comment(tags_str)
            debug_print(comment)
            await message.channel.send(comment, reference=message)
        except Exception as e:
            await message.channel.send("処理中にエラーが発生しました")


    """
    画像を保存
    """
    async def save_image(self, attachment):
        # フォルダを作る
        save_dir = Path(Settings.image_folder)
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
        


    async def on_ready(self):
        print(f'{self.bot.user.name}がログインしました')

    async def cmd_hoge(self, ctx):
        await ctx.send('ほげほげ')


my_bot = MyDiscordBot()
my_bot.bot.run(Settings.discord_token)

