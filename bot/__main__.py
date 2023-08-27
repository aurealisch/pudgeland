from .common import commons
from .utility.constant import activities

commons.client.plugins.load_folder('bot.plugin')

activity = activities.activity

commons.bot.run(activity=activity)
