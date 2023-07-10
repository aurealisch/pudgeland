import crescent
import hikari

from pudgeland.plugins import voice
from pudgeland.common import config

from ..modules import locales

plugin = crescent.Plugin[hikari.GatewayBot, None]()


@voice.group.child
@plugin.include
@crescent.command(
    name=locales.LocaleBuilder(
        "create",
        russian="создать",
        ukrainian="утворити",
    ),
    description=locales.LocaleBuilder(
        "Create",
        russian="Создать",
        ukrainian="Утворити",
    ),
)
class Create:
    name = crescent.option(
        str,
        name=locales.LocaleBuilder(
            "name",
            russian="имя",
            ukrainian="iмя",
        ),
        description=locales.LocaleBuilder(
            "Name",
            russian="Имя приватного голосового канала",
            ukrainian="Iм'я приватного голосового каналу",
        ),
    )
    position = crescent.option(
        int,
        name=locales.LocaleBuilder(
            "position",
            russian="позиция",
            ukrainian="позицiя",
        ),
        description=locales.LocaleBuilder(
            "Position",
            russian="Позиция приватного голосового канала",
            ukrainian="Позицiя приватного голосового каналу",
        ),
        default=None,
    )
    user_limit = crescent.option(
        int,
        name=locales.LocaleBuilder(
            "user-limit",
            russian="пользовательский-лимит",
            ukrainian="користувальницкий-лiмiт",
        ),
        description=locales.LocaleBuilder(
            "User limit",
            russian="Пользовательский лимит приватного голосового канала",
            ukrainian="Користувальницкий лiмiт приватного голосового каналу",
        ),
        min_value=0,
        max_value=99,
        default=None,
    )
    bitrate = crescent.option(
        int,
        name=locales.LocaleBuilder(
            "bitrate",
            russian="скорость-передачи-данных",
            ukrainian="швидкiсть-передачi-даних",
        ),
        description=locales.LocaleBuilder(
            "Bitrate",
            russian="Скорость передачи данных приватного голосового канала",
            ukrainian="Швидкiсть передачi даних приватного голосового каналу",
        ),
        min_value=8_000,
        max_value=96_000,
        default=None,
    )
    video_quality_mode = crescent.option(
        int,
        name=locales.LocaleBuilder(
            "video-quality-mode",
            russian="режим-качества-видео",
            ukrainian="режим-якості-відео",
        ),
        description=locales.LocaleBuilder(
            "Video quality mode",
            russian="Режим качества видео приватного голосового канала",
            ukrainian="Режим якості відео приватного голосового каналу",
        ),
        choices=[
            (
                locales.LocaleBuilder(
                    "Video quality will be set for optimal performance.",
                    russian="Качество видео будет настроено для оптимальной производительности.",  # noqa: E501
                    ukrainian="Якість відео буде налаштовано для оптимальної продуктивності.",  # noqa: E501
                ),
                hikari.VideoQualityMode.AUTO,
            ),
            (
                locales.LocaleBuilder(
                    "Video quality will be set to 720p.",
                    russian="Качество видео будет установлено на 720p.",
                    ukrainian="Якість відео буде встановлено на 720p.",
                ),
                hikari.VideoQualityMode.FULL,
            ),
        ],
        default=None,
    )

    # noinspection PyMethodMayBeStatic
    async def callback(self, context: crescent.Context) -> None:
        name = self.name
        position = self.position
        user_limit = self.user_limit
        bitrate = self.bitrate
        video_quality_mode = self.video_quality_mode

        guild_id = config.private_voice_channel_guild_id
        category_id = config.private_voice_channel_category_id

        guild_voice_channel = await plugin.app.rest.create_guild_voice_channel(
            guild_id,
            name=name,
            position=position,
            user_limit=user_limit,
            bitrate=bitrate,
            video_quality_mode=video_quality_mode,
            category=category_id,
        )

        guild_voice_channel_id = guild_voice_channel.id

        embed = hikari.Embed(
            title="Создать",
            description=f"""\
                <#{guild_voice_channel_id}>
            """,
        )

        await context.respond(ephemeral=True, embed=embed)
