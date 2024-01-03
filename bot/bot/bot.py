import hikari
from crescent import Client as crescent_Client
from flare import install as flare_install

from bot.modules.model import Model


class Bot:
    def __init__(self, model: Model, token: str) -> None:
        intents = hikari.Intents.ALL

        gateway_bot = hikari.GatewayBot(token, intents=intents)

        gateway_bot.listen(hikari.StartedEvent)(model.on_started_event)
        gateway_bot.listen(hikari.StoppedEvent)(model.on_stopped_event)

        flare_install(gateway_bot)

        client = crescent_Client(gateway_bot, model=model)

        for cmd in [
            "leaders.banana",
            "leaders.monkey",
            "leaders.coin",
            "leaders.diamond",
            "leaders.netherite",
            "purchase.coin",
            "purchase.diamond",
            "purchase.netherite",
            "sale.coin",
            "sale.diamond",
            "sale.netherite",
            "collecting",
            "domestication",
            "profile",
        ]:
            client.plugins.load(f"bot.cmds.{cmd}")

        self.run = gateway_bot.run
