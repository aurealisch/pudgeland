import crescent
import hikari

from .modules import config

gateway_bot = hikari.GatewayBot(config.token)

client = crescent.Client(gateway_bot)

gateway_bot.run()
