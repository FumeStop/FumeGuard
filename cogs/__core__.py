import json
from itertools import cycle

import discord
from discord.ext import commands, tasks

from utils.db import guild_exists, add_guild
from utils.logger import log_member, welcome_member


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("config.json") as json_file:
            data = json.load(json_file)
            self.community_server_id = data["community_server_id"]

        self.status_items = None

    @tasks.loop(seconds=10)
    async def _change_status(self):
        await self.bot.change_presence(
            status=discord.Status.online, activity=discord.Game(next(self.status_items))
        )

    @commands.Cog.listener()
    async def on_ready(self):
        self.status_items = cycle(
            [
                f"on {len(self.bot.guilds)} servers | /help",
                "/invite | /vote | /review | /community",
                "https://fumes.top/fumeguard",
            ]
        )

        self._change_status.start()

        self.bot.log.info("FumeGuard is ready")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if not await guild_exists(guild_id=guild.id):
            await add_guild(guild_id=guild.id)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await log_member(member)
        await welcome_member(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await log_member(member, join=False)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.guild and message.guild.me in message.mentions:
            await message.reply(content="Hello there! Use `/help` to get started.")


async def setup(bot):
    await bot.add_cog(Core(bot))
