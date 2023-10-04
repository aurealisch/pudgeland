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
        token: str,
    ) -> None:
        INTENTS = hikari.Intents.ALL

        self.__gatewayBot = hikari.GatewayBot(token, intents=INTENTS)

        self.__gatewayBot.listen(hikari.StartedEvent)(model.onStartedEvent)
        self.__gatewayBot.listen(hikari.StoppedEvent)(model.onStoppedEvent)

        miru.install(self.__gatewayBot)

        CLIENT = crescent.Client(self.__gatewayBot, model=model)

        for PLUGIN in plugins:
            CLIENT.plugins.load(PLUGIN)

    def run(self) -> None:
        self.__gatewayBot.run()
