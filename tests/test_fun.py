import asyncio
import discord.ext.test as dpytest
import discord.ext.commands as commands
import unittest

prefixes = ["fur ", "Fur ", "FUR "]

bot = commands.Bot(command_prefix=prefixes)


async def test_ping():
    dpytest.configure(bot)
    await dpytest.message("fur penis")
    assert dpytest.verify().message().contains().content("a")




asyncio.run(test_ping())