"""."""

from .common import commons
from .utility.constant import presences


modules = [
  'actions',
  'economics.bananas',
  'economics.monkeys',
  'other',
  'other.images.animals',
  'other.leaders',
  'other.reputation',
  'other.shop',
]

for module in modules:
  commons.client.plugins.load_folder(f'bot.module.{module}.plugin')

activity = presences.activity

commons.bot.run(activity=activity)
