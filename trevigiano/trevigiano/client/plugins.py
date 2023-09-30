import crescent

from trevigiano.client import models

from .abc import views
from .command import (
    commands,
    contexts,
    exceptions,
    options,
)


class Plugin(crescent.Plugin[None, models.Model]):
    views = views
    commands = commands
    contexts = contexts
    exceptions = exceptions
    options = options
