import typing

import crescent
import hikari
import miru

from trevigiano import model


class Trevigiano:
    def __init__(
            self,
            plugins: typing.Iterable[str],
            model: model.Model,
            token: str) -> None:
        intents = hikari.Intents.ALL

        self.__gateway_bot = hikari.GatewayBot(token, intents=intents)

        self.__gateway_bot.listen(hikari.StartedEvent)(model.on_started_event)
        self.__gateway_bot.listen(hikari.StoppedEvent)(model.on_stopped_event)

        miru.install(self.__gateway_bot)

        client = crescent.Client(self.__gateway_bot, model=model)

        for plugin in plugins:
            client.plugins.load(plugin)

    def run(self) -> None:
        self.__gateway_bot.run()
