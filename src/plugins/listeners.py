import hikari
import lightbulb
import logging
from lightbulb import context

from lightbulb.app import BotApp

log = logging.getLogger(__name__)


class Listeners(lightbulb.Plugin):
    def __init__(self, bot: lightbulb.BotApp):
        super().__init__(name="listeners")
        self.bot_client = bot
        self.bot_client.subscribe(lightbulb.CommandErrorEvent, self.on_command_error)
        self.bot_client.subscribe(
            lightbulb.UserCommandInvocationEvent, self.on_command_invoked
        )

    async def on_command_invoked(self, event: lightbulb.UserCommandInvocationEvent):
        user = event.context.author.username
        log.info(user + " used command " + event.command.name)

    async def on_command_error(self, event: lightbulb.CommandErrorEvent):
        error = event.exception
        context = event.context
        command = event.context.command
        print(error)
        if isinstance(error, lightbulb.errors.CommandIsOnCooldown):
            return await event.context.respond("Command is on cooldown")

        elif isinstance(error, lightbulb.CommandNotFound):
            return await event.context.respond("Comando no existente")

        elif isinstance(error, lightbulb.errors.BotMissingRequiredPermission):
            missing_perms = ", ".join(c for c in error.permissions)
            print(f"bot - {missing_perms}")
            return await event.context.respond(
                f":no_entry_sign: Command failed, i'm missing `{missing_perms}` permissions!"
            )

        elif isinstance(error, lightbulb.errors.MissingRequiredPermission):
            missing_perms = ", ".join(c for c in error.permissions)
            print(f"user - {missing_perms}")
            return await event.context.respond(
                f":no_entry_sign: Error, no dispones del permiso `{missing_perms}` "
            )

        elif isinstance(error, lightbulb.errors.NotEnoughArguments):
            await event.context.respond(
                "Error: Faltan argumentos, comprueba como se usa el comando {}".format(
                    command.name
                )
            )
            await lightbulb.DefaultHelpCommand.send_command_help(self, context, command)
            # await lightbulb.HelpCommand.send_command_help(self, context, command)
            return


def load(bot: lightbulb.BotApp):
    listeners = Listeners(bot)
    bot.add_plugin(listeners)
    # bot.listen(lightbulb.CommandErrorEvent, listeners.on_command_error)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin("Listeners")
