import env

from trevigiano import (
    configurations,
    databases,
    models,
    trevigiano,
    )

commands = [
    'profile',
    'berries.collect',
    'berries.steal',
    'foxes.tame',
    'leaders.berries',
    'leaders.foxes',
    'leaders.reputation',
    'reputation.downgrade',
    'reputation.upgrade',
    ]
plugins = [f'commands.{command}' for command in commands]

database = databases.Database(env.get('HOST'),
                              port=env.get('PORT'),
                              user=env.get('USER'),
                              password=env.get('PASSWORD'),
                              database=env.get('DATABASE'),
                              )

configuration: configurations.Configuration = {
    'plugins': {
        'collect': {
            'berry': {'start': 100, 'stop': 250},
            'fox': {'start': 25, 'stop': 100}
        },
        'steal': {'fraction': 0.1, 'probability': 3},
        'tame': {'price': 100, 'probability': 5}
    }
}

model = models.Model(configuration, database=database)

token = env.get('TOKEN')

trevigiano.Trevigiano(plugins,
                      model=model,
                      token=token,
                      ).run()
