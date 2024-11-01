import os
import asyncio
from loguru import logger
import discord
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor
from modules.Settings import Settings
from modules.Message import Message
from modules.Tagger import Tagger
from modules.CommandR import CommandRPlus
from modules.Prompt import Prompt
from modules.utils import debug_print, save_image

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
        self.chara = "random"

        # Discordのインテント設定
        intents = discord.Intents.default()
        intents.message_content = True

        Message.init()
        Prompt.init()

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

        @self.bot.group(invoke_without_command=True)
        @in_allowed_channel()
        async def chara(ctx, name = None):
            if ctx.invoked_subcommand is None:
                if name is None:
                    await ctx.send(Message.msg.DISCORD_CHARA_DEFAULT)
                else:
                    await self.cmd_chara_set(ctx, name)

        @chara.command(name='list')
        async def chara_list(ctx):
            await self.cmd_chara_list(ctx)

        @chara.command(name='random')
        async def chara_random(ctx):
            await self.cmd_chara_random(ctx)

        @hoge.error
        async def hoge_error(ctx, error):
            if isinstance(error, commands.CheckFailure):
                await ctx.send(Message.msg.DISCORD_NOT_ALLOWED_CMD)

        @chara.error
        async def chara_error(ctx, error):
            if isinstance(error, commands.CheckFailure):
                await ctx.send(Message.msg.DISCORD_NOT_ALLOWED_CMD)
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
            await message.channel.send(f'{message.author.mention} {Message.msg.DISCORD_ATTACH_MANY}', reference=message)
        elif image_attachments:
            await message.channel.send(f'{message.author.mention} {Message.msg.DISCORD_ATTACH_NORMAL}', reference=message)
        else:
            await message.channel.send(f'{message.author.mention} {Message.msg.DISCORD_ATTACH_NOT_IMAGE}', reference=message)
            return

        # 最初の画像のみを処理
        await self.process_image(message, image_attachments[0])


    """
    画像処理
    """
    async def process_image(self, message, attachment):
        # 画像を保存
        success, responce, file_path = await save_image(attachment, Settings.image_folder)

        # 画像保存失敗メッセージ
        if not success:
            await message.channel.send(responce)
            return

        # LLMからコメント取得を別タスクで実行
        asyncio.create_task(self.process_llm(message, file_path))

    """
    LLMからコメント取得
    """
    async def process_llm(self, message, file_path):
        try:
            # イベントループを取得
            loop = asyncio.get_event_loop()

            # タグ取得を別スレッドで実行
            tags = await loop.run_in_executor(
                ThreadPoolExecutor(),
                Tagger.get_tags,
                file_path
            )
            tags_str = ', '.join(tags.keys())
            logger.debug(tags_str)

            # LLMの処理も別スレッドで実行
            comment = await loop.run_in_executor(
                ThreadPoolExecutor(),
                self.llm.get_comment,
                Prompt.get_prompt(self.chara),
                tags_str
            )
            logger.debug(comment)
            await message.channel.send(comment, reference=message)

        except Exception as e:
            await message.channel.send(Message.msg.LLM_COMMENT_ERROR)

    async def on_ready(self):
        logger.info(f'{self.bot.user.name}がログインしました')

    async def cmd_hoge(self, ctx):
        await ctx.send('ほげほげ')

    """キャラクター一覧を表示"""
    async def cmd_chara_list(self, ctx):
        await ctx.send(f'{Message.msg.DISCORD_CHARA_LIST}{Prompt.get_chara_list()}')

    """キャラクターをランダムにする"""
    async def cmd_chara_random(self, ctx):
        self.chara = "random"
        await ctx.send(Message.msg.DISCORD_CHARA_RANDOM)

    """キャラクターを指名する"""
    async def cmd_chara_set(self, ctx, name: str):
        if Prompt.is_exists_chara(name):
            self.chara = name
            await ctx.send(Message.get("DISCORD_CHARA_RANDOM", name=name))
        else:
            await ctx.send(Message.get("DISCORD_CHARA_NOT_EXISTS", name=name))


# ファイルへの出力設定
logger.add("./log/homeko.log", rotation="100 MB")

my_bot = MyDiscordBot()
my_bot.bot.run(Settings.discord_token)

