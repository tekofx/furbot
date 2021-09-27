import lightbulb


class Listeners(lightbulb.Plugin):
    def __init__(self):
        super().__init__(name="listeners")

    @lightbulb.listener(lightbulb.events.CommandErrorEvent)
    async def on_command_error(self, event):
        error = event.exception
        if isinstance(error, lightbulb.errors.CommandIsOnCooldown):
            return await event.context.reply("Command is on cooldown")

        if isinstance(error, lightbulb.errors.CommandNotFound):
            return await event.context.reply("Command is on cooldown")

        if isinstance(error, lightbulb.errors.BotMissingRequiredPermission):
            missing_perms = ", ".join(c for c in error.permissions)
            print(f"bot - {missing_perms}")
            return await event.message.reply(
                f":no_entry_sign: Command failed, i'm missing `{missing_perms}` permissions!"
            )

        if isinstance(error, lightbulb.errors.MissingRequiredPermission):
            missing_perms = ", ".join(c for c in error.permissions)
            print(f"user - {missing_perms}")
            return await event.message.reply(
                f":no_entry_sign: Command failed, you're missing `{missing_perms}` permissions!"
            )

        if isinstance(error, lightbulb.errors.NotEnoughArguments):
            return await event.message.respond("Error: Not enough arguments")


def load(bot: lightbulb.Bot):
    bot.add_plugin(Listeners)
