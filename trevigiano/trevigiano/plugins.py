import crescent

from trevigiano import (
    commands,
    contexts,
    exceptions,
    models,
    options,
    views,
    )


class Plugin(crescent.Plugin[None, models.Model]):
    commands = commands
    contexts = contexts
    exceptions = exceptions
    options = options
    views = views
