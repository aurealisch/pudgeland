from .configuration.dto import configurations

configuration = configurations.ConfigurationDTO(
  configurations.ActivityDTO('гг сервер умер'),
  leaders=configurations.LeadersDTO(
    configurations.SortDTO('desc'),
    take=5,
  ),
  plugins=configurations.PluginsDTO(
    configurations.CollectDTO(
      configurations.RangeDTO(
        75,
        b=200
      ),
      ying=configurations.RangeDTO(
        50,
        b=135,
      )
    ),
    cull=configurations.CullDTO(
      4,
      fraction=0.4,
    ),
    tame=configurations.TameDTO(
      4,
      price=500,
    )
  ),
  bunches=configurations.BunchesDTO(
    'бананы',
    y='обезьяны',
  ),
  emojis=configurations.EmojisDTO(
    '🍌',
    y='🐒',
  )
)
