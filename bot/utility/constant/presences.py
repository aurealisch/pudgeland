"""."""

import hikari

from bot.common import commons

name = commons.configuration.activity.name

activity = hikari.Activity(name=name)
