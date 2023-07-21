# -*- coding: utf-8 -*-
# MIT License
#
# Copyright (c) 2023 pudgeland
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
import os

import dotenv
import hikari
import msgspec

import prisma as _prisma
from bot.client import clients
from bot.common.configuration import configurations
from bot.common.database import databases
from bot.common.database.middleware import middlewares
from bot.common.environment import environments
from bot.common.model import models

# Parse a .env file and then load all the variables found as environment variables.
dotenv.load_dotenv()

with open("configuration.json") as stream:
    buffer = stream.read()

    configuration = msgspec.json.decode(buffer, type=configurations.Configuration)

prisma = _prisma.Prisma()

# Register a client instance to be retrieved by `get_client()`.
_prisma.register(prisma)

database = databases.Database(middlewares.Middleware(prisma))

token = os.environ.get("TOKEN")
url = os.environ.get("URL")

environment = environments.Environment(token, url=url)

model = models.Model(configuration, database=database, environment=environment)

bot = hikari.GatewayBot(environment.token, banner=configuration.gateway.bot.banner)

# Subscribe a given callback to a given event type.
bot.subscribe(hikari.StartedEvent, callback=model.on_started_event)
bot.subscribe(hikari.StoppedEvent, callback=model.on_stopped_event)

client = clients.Client(bot, model=model)

# Loads plugins from a folder.
client.plugins.load_folder("bot.plugin")
