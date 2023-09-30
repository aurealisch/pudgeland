import crescent

from trevigiano.client import model

from . import view_abc
from .commands import (
    command,
    context,
    exceptions,
    option,
)


class Plugin(crescent.Plugin[None, model.Model]):
    view_abc = view_abc
    command = command
    context = context
    exceptions = exceptions
    option = option
