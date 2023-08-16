"""."""

import attrs
import hikari

from bot.core import configurations
from bot.core import databases
from bot.core import environments


@attrs.define
class Model:
  """."""

  configuration: configurations.Configuration
  database: databases.Database
  environment: environments.Environment

  async def on_started_event(self, _: hikari.StartedEvent) -> None:
    """."""

    await self.database.prisma.connect()

  async def on_stopped_event(self, _: hikari.StoppedEvent) -> None:
    """."""

    await self.database.prisma.disconnect()
