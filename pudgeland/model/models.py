import attrs
import collei


@attrs.define
class Model:
    client: collei.Client

