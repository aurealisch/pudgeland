import typing

import crescent
import hikari
import miru

from . import model


class Trevigiano:
    def __init__(
        self: typing.Self,
        plugins: typing.Iterable[str],
        model: "model.Model",
        token: str,
    ) -> None:
        self.model = model

        INTENTS = (
            hikari.Intents.MESSAGE_CONTENT
            | hikari.Intents.GUILDS
            | hikari.Intents.GUILD_MESSAGES
        )

        GATEWAY_BOT = hikari.GatewayBot(token, intents=INTENTS)

        miru.install(GATEWAY_BOT)

        CLIENT = crescent.Client(GATEWAY_BOT, model=model)

        for PLUGIN in plugins:
            CLIENT.plugins.load(PLUGIN)

        GATEWAY_BOT.listen(hikari.StartedEvent)(model.on_started_event)
        GATEWAY_BOT.listen(hikari.StoppedEvent)(model.on_stopped_event)

        self.__gateway_bot = GATEWAY_BOT

    def run(self: typing.Self) -> None:
        return self.__gateway_bot.run()
