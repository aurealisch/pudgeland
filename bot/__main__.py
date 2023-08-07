import threading

import uvicorn

from .api.app import apps
from .common import commons
from .utility.constant import presences


def target() -> None:
    app = apps.app

    host = commons.configuration.api.host
    port = commons.environment.port

    return uvicorn.run(app, host=host, port=port)


thread = threading.Thread(target=target)
thread.start()

modules = [
    "actions",
    "economics",
    "leaders",
    "miscellaneous",
    "reputation",
]

for module in modules:
    commons.client.plugins.load_folder(f"bot.module.{module}.plugin")

activity = presences.activity

commons.bot.run(activity=activity)
