import typing

import crescent
import flare
import hikari

from bot import models


class Bot:
    def __init__(
        self, cmds: typing.Sequence[str], model: models.Model, token: str
    ) -> None:
        INTENTS = hikari.Intents.ALL

        gatewayBot = hikari.GatewayBot(token, intents=INTENTS)

        gatewayBot.listen(hikari.StartedEvent)(model.onStartedE)
        gatewayBot.listen(hikari.StoppedEvent)(model.onStoppedE)

        flare.install(gatewayBot)

        client = crescent.Client(gatewayBot, model=model)

        for cmd in cmds:
            client.plugins.load(f"bot.cmds.{cmd}")

        self.run = gatewayBot.run
