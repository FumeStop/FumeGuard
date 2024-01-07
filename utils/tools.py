from typing import Union, Optional

import discord
from discord import app_commands

from utils.db import is_premium_user


def parse_cooldown(retry_after: Union[int, float]):
    retry_after = int(retry_after)

    hours, remainder = divmod(retry_after, 3600)
    minutes, seconds = divmod(remainder, 60)

    return minutes, seconds


async def cooldown_level_0(
    ctx: discord.Interaction,
) -> Optional[app_commands.Cooldown]:
    if await ctx.client.is_owner(ctx.user):
        return

    elif await is_premium_user(ctx.user.id):
        return app_commands.Cooldown(1, 2.0)

    else:
        return app_commands.Cooldown(1, 5.0)


async def cooldown_level_1(
    ctx: discord.Interaction,
) -> Optional[app_commands.Cooldown]:
    if await ctx.client.is_owner(ctx.user):
        return

    elif await is_premium_user(ctx.user.id):
        return app_commands.Cooldown(1, 60.0)

    else:
        return app_commands.Cooldown(1, 3600.0)
