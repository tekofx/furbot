import hikari
import lightbulb
from lightbulb.help import HelpCommand


class Listeners(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.Bot):
        super().__init__(name="listeners")
        self.bot = bot

    @lightbulb.listener(lightbulb.events.CommandErrorEvent)
    async def on_command_error(self, event: lightbulb.events.CommandErrorEvent):
        error = event.exception
        command = event.command
        if isinstance(error, lightbulb.errors.CommandIsOnCooldown):
            return await event.message.reply("Command is on cooldown")

        if isinstance(error, lightbulb.errors.CommandNotFound):
            return await event.message.respond("Comando no existente")

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
                f":no_entry_sign: Error, no dispones del permiso `{missing_perms}` "
            )

        if isinstance(error, lightbulb.errors.NotEnoughArguments):
            await event.message.respond(
                "Error: Faltan argumentos, comprueba como se usa el comando {}".format(
                    command.name
                )
            )
            await lightbulb.HelpCommand.send_command_help(self, event.context, command)
            return


def load(bot: lightbulb.Bot):
    bot.add_plugin(Listeners(bot))


def unload(bot: lightbulb.Bot):
    bot.remove_plugin("Listeners")
