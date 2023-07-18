# MIT License
#
# Copyright (c) 2023 elaresai
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from __future__ import annotations

__all__: typing.Sequence[str] = (
    "environment",
    "bot",
    "prisma",
    "database",
    "model",
    "client",
)

import os
import typing

import hikari

import prisma as _prisma
from bot.client import clients
from bot.common.database import databases
from bot.common.environment import environments
from bot.common.model import models

environment = environments.Environment(
    os.environ.get("GATEWAY_BOT_TOKEN"),
    os.environ.get("GATEWAY_BOT_BANNER"),
    os.environ.get("JAVA_SERVER_HOST"),
    os.environ.get("JAVA_SERVER_PORT"),
    os.environ.get("DATABASE_URL"),
    os.environ.get("API_HOST"),
    os.environ.get("API_PORT"),
    os.environ.get("BY_HAND_MINIMAL"),
    os.environ.get("BY_HAND_MAXIMUM"),
    os.environ.get("DEFAULT_MODE_COLOR"),
    os.environ.get("ERROR_MODE_COLOR"),
    os.environ.get("SUCCESS_MODE_COLOR"),
)

bot = hikari.GatewayBot(
    environment.gateway_bot_token,
    banner=environment.gateway_bot_banner,
)

prisma = _prisma.Prisma()

_prisma.register(prisma)

database = databases.Database(prisma)

model = models.Model(database, environment=environment)

bot.subscribe(hikari.StartedEvent, model.on_started_event)
bot.subscribe(hikari.StoppedEvent, model.on_stopped_event)

client = clients.Client(bot, model=model)
