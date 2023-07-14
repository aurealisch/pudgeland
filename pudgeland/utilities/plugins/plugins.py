import crescent
import hikari

from ...models import model


class Plugin(crescent.Plugin[hikari.GatewayBot, model.Model]):
    pass
