import env as environment

from trevigiano import configurations, databases, models, trevigiano

commands = [
    'profile',
    'domestication.foxes',
    'collecting.berries',
    'leaders.berries',
    'leaders.foxes',
    'leaders.coins',
    'leaders.diamonds',
    'leaders.netherite.scraps',
    'purchase.coins',
    'purchase.diamonds',
    'purchase.netherite.scraps',
    'sale.coins',
    'sale.diamonds',
    'sale.netherite.scraps',
]
plugins = [f'commands.{command}' for command in commands]

database = databases.Database(environment.get('AUTHORIZATION'))

configuration: configurations.Configuration = {
    'plugins': {
        'collect': {
            'range': {
                'start': 25,
                'stop': 100
            }
        },
        'multipliers': {
            'purchase': {
                'coins': 500,
                'diamonds': 4,
                'netherite': {
                    'scraps': 8
                }
            },
            'tame': 200
        }
    }
}

model = models.Model(configuration, database=database)

token = environment.get('TOKEN')

trevigiano.Trevigiano(plugins, model=model, token=token).run()
