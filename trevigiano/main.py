import env as environment

from trevigiano import configurations, databases, models, trevigiano

commands = [
    'profile', 'berries.collect', 'berries.steal', 'foxes.tame',
    'leaders.berries', 'leaders.foxes'
]
plugins = [f'commands.{command}' for command in commands]

database = databases.Database(environment.get('AUTHORIZATION'))

configuration: configurations.Configuration = {
    'plugins': {
        'collect': {
            'range': {
                'start': 10,
                'stop': 100
            }
        },
        'steal': {
            'fraction': 0.1,
            'probability': 3
        },
        'tame': {
            'multiplicateur': 50,
        }
    }
}

model = models.Model(configuration, database=database)

token = environment.get('TOKEN')

trevigiano.Trevigiano(plugins, model=model, token=token).run()
