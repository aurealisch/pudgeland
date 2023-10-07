import crescent

from trevigiano import (
    command,
    context,
    coolDown,
    exceptions,
    model,
    option,
    view,
    )


class Plugin(crescent.Plugin[None, model.Model]):
    view = view
    command = command
    context = context
    exceptions = exceptions
    option = option
    coolDown = coolDown
