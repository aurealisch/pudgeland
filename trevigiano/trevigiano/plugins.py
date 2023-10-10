import crescent

from trevigiano import (
    commands,
    contexts,
    exceptions,
    models,
)


class Plugin(crescent.Plugin[None, models.Model]):
    commands = commands
    contexts = contexts
    exceptions = exceptions
