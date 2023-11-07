import typing

import crescent
import flare
import hikari

from bot import models


class Bot:

    def __init__(self, plugins: typing.Iterable[str], model: models.Model,
                 token: str) -> None:
        """Description"""
        intents = hikari.Intents.ALL

        self.__gateway_bot = hikari.GatewayBot(token, intents=intents)

        self.__gateway_bot.listen(hikari.StartedEvent)(model.onStartedEvent)
        self.__gateway_bot.listen(hikari.StoppedEvent)(model.onStoppedEvent)

        flare.install(self.__gateway_bot)

        client = crescent.Client(self.__gateway_bot, model=model)

        for plugin in plugins:
            client.plugins.load(plugin)

    def run(self) -> None:
        """Description"""
        self.__gateway_bot.run()
