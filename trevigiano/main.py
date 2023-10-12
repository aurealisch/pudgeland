import env as environment

from trevigiano import configurations, databases, models, trevigiano

commands = [
    'profile', 'berries.collect', 'berries.steal', 'foxes.tame',
    'leaders.berries', 'leaders.foxes'
]
plugins = [f'commands.{command}' for command in commands]

database = databases.Database(environment.get('HOST'),
                              port=environment.get('PORT'),
                              user=environment.get('USER'),
                              password=environment.get('PASSWORD'),
                              database=environment.get('DATABASE'))

configuration: configurations.Configuration = {
    'plugins': {
        'collect': {
            'range': {
                'start': 50,
                'stop': 200
            }
        },
        'steal': {
            'fraction': 0.1,
            'probability': 3
        },
        'tame': {
            'price': 100,
            'probability': 5
        }
    }
}

model = models.Model(configuration, database=database)

token = environment.get('TOKEN')

trevigiano.Trevigiano(plugins, model=model, token=token).run()
