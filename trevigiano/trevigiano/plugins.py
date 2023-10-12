import crescent

from trevigiano import commands, contexts, errors, models


class Plugin(crescent.Plugin[None, models.Model]):
    commands = commands
    contexts = contexts
    errors = errors
