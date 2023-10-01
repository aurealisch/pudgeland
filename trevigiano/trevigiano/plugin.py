import crescent

from trevigiano import model

from . import (
    command,
    context,
    exceptions,
    option,
    view_abc,
)


class Plugin(crescent.Plugin[None, model.Model]):
    view_abc = view_abc
    command = command
    context = context
    exceptions = exceptions
    option = option
