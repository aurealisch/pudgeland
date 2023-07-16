import threading

import uvicorn

from bot.api.app import apps
from bot.common import commons
from bot.common.environment import environments

commons.client.plugins.load_folder("pudgeland.plugin.action")
commons.client.plugins.load_folder("pudgeland.plugin.animal")
commons.client.plugins.load_folder("pudgeland.plugin.economics")
commons.client.plugins.load_folder("pudgeland.plugin.server")

threading.Thread(
    target=lambda: uvicorn.run(
        apps.app,
        host=environments.api_host,
        port=environments.api_port,
    )
).start()

commons.bot.run()
