import crescent
import hikari

from bot.common import models

from .abc import views as _views
from .command import commands as _commands
from .command import contexts as _contexts
from .command import cooldowns as _cooldowns
from .command import exceptions as _exceptions
from .command import options as _options


class Plugin(
    crescent.Plugin[
        hikari.GatewayBot,
        models.Model,
    ]
):
    views = _views
    commands = _commands
    contexts = _contexts
    cooldowns = _cooldowns
    exceptions = _exceptions
    options = _options
