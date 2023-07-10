import json

import attrs


@attrs.define
class Config:
    gateway_bot_token: str = attrs.field(alias="gatewayBotToken")

    java_server_host: str = attrs.field(alias="javaServerHost")
    java_server_port: int = attrs.field(alias="javaServerPort")


with open("./config.json", encoding="utf-8") as stream:
    config = Config(**json.loads(stream.read()))

gateway_bot_token = config.gateway_bot_token

java_server_host = config.java_server_host
java_server_port = config.java_server_port
