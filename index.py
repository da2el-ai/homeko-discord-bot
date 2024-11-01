from loguru import logger
import discord
from discord.ext import commands
from modules.Settings import Settings
from modules.Message import Message
from modules.Prompt import Prompt
from modules.HomekoControl import HomekoControl

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
        Message.init()
        Prompt.init()

        # Discordのインテント設定
        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.setup_commands()
        self.setup_events()

        # 実際の作業を行うコントローラー「褒め子」さん
        self.homeko = HomekoControl(self.bot)


    """
    コマンド設定
    """
    def setup_commands(self):
        @self.bot.event
        async def on_ready():
            await self.homeko.on_ready()

        @self.bot.command()
        @in_allowed_channel()
        async def hoge(ctx):
            await self.homeko.cmd_hoge(ctx)

        @self.bot.group(invoke_without_command=True)
        @in_allowed_channel()
        async def chara(ctx, name = None):
            await self.homeko.cmd_chara(ctx, name)

        @chara.command(name='list')
        async def chara_list(ctx):
            await self.homeko.cmd_chara_list(ctx)

        @chara.command(name='random')
        async def chara_random(ctx):
            await self.homeko.cmd_chara_random(ctx)

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
                await self.homeko.handle_attachment(message)

            # この行は必須！コマンドの処理を行うため
            await self.bot.process_commands(message)



# ファイルへの出力設定
logger.add("./log/homeko.log", rotation="100 MB")

my_bot = MyDiscordBot()
my_bot.bot.run(Settings.discord_token)

