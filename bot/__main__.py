"""."""

from .common import commons
from .utility.constant import presences

commons.client.plugins.load_folder(f'bot.plugin')

activity = presences.activity

commons.bot.run(activity=activity)
