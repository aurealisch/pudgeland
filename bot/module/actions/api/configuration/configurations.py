import attrs
import yarl


@attrs.define
class Configuration:
    url: yarl.URL
