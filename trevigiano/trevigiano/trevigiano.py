import typing

import crescent
import flare
import hikari

from trevigiano import models


class Trevigiano:

    def __init__(self, plugins: typing.Iterable[str], model: models.Model,
                 token: str) -> None:
        """Description

        Parameters
        ----------
        plugins : typing.Iterable[str]
            Description
        model : models.Model
            Description
        token : str
            Description
        """
        intents = hikari.Intents.ALL

        self.__gateway_bot = hikari.GatewayBot(token, intents=intents)

        flare.install(self.__gateway_bot)

        client = crescent.Client(self.__gateway_bot, model=model)

        for plugin in plugins:
            client.plugins.load(plugin)

    def run(self) -> None:
        """Description"""
        self.__gateway_bot.run()
