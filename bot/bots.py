import typing

import crescent
import hikari
import miru

from .common import models


@typing.final
class Bot:
    def __init__(
        self,
        token: str,
        model: "models.Model",
    ) -> None:
        self.model = model

        self.configuration = self.model.configuration
        self.economics = self.model.economics

        intents = (
            hikari.Intents.MESSAGE_CONTENT
            | hikari.Intents.GUILDS
            | hikari.Intents.GUILD_MESSAGES
        )

        self.gateway_bot = hikari.GatewayBot(token, intents=intents)

        miru.install(self.gateway_bot)

        self.gateway_bot.subscribe(hikari.StartedEvent, callback=self.model.started)
        self.gateway_bot.subscribe(hikari.StoppedEvent, callback=self.model.stopped)

        self.client = crescent.Client(self.gateway_bot, model=self.model)

        self.client.plugins.load_folder("bot.plugin")

    def run(self) -> None:
        return self.gateway_bot.run(
            activity=hikari.Activity(name=self.configuration.activity.name)
        )
