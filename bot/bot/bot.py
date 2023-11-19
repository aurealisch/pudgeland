import crescent
import flare
import hikari

from bot import models, types


class Bot:

    def __init__(self, plugins: types.Plugins, model: models.Model,
                 token: types.Token) -> None:
        INTENTS = hikari.Intents.ALL

        gatewayBot = hikari.GatewayBot(token, intents=INTENTS)

        gatewayBot.listen(hikari.StartedEvent)(model.onStartedE)
        gatewayBot.listen(hikari.StoppedEvent)(model.onStoppedE)

        flare.install(gatewayBot)

        client = crescent.Client(gatewayBot, model=model)

        for plugin in plugins:
            client.plugins.load(f"bot.plugin.{plugin}")

        self.run = gatewayBot.run
