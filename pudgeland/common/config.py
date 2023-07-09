import json

import attrs


@attrs.define
class Config:
    token: str
    address: str


with open("./config.json", encoding="utf-8") as stream:
    config = Config(**json.loads(stream.read()))

token = config.token
address = config.address
