import typing

import attrs
import crescent
import hikari


@attrs.define
class LocaleBuilder(crescent.LocaleBuilder):
    _fallback: str

    russian: str
    ukrainian: str

    def build(self) -> typing.Mapping[str, str]:
        return {
            hikari.Locale.RU: self.russian,
            hikari.Locale.UK: self.ukrainian,
        }

    @property
    def fallback(self) -> str:
        return self._fallback
