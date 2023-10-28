import env as environment

from trevigiano import configurations, databases, models, trevigiano

commands = [
    "profile", "domestication.foxes", "collecting.berries", "leaders.berries",
    "leaders.foxes", "leaders.coins", "leaders.diamonds",
    "leaders.netherite.scraps", "purchase.coins", "purchase.diamonds",
    "purchase.netherite.scraps", "sale.coins", "sale.diamonds",
    "sale.netherite.scraps"
]
plugins = [f"commands.{command}" for command in commands]

database = databases.Database(environment.get("HOST"),
                              port=environment.get("PORT"),
                              user=environment.get("USER"),
                              password=environment.get("PASSWORD"),
                              database=environment.get("DATABASE"))

configuration: configurations.Configuration = {
    "plugins": {
        "collect": {
            "range": {
                "start": 5,
                "stop": 50
            }
        },
        "multipliers": {
            "purchase": {
                "coins": 125,
                "diamonds": 4,
                "netherite": {
                    "scraps": 8
                }
            },
            "tame": 250
        }
    }
}

model = models.Model(configuration, database=database)

token = environment.get("TOKEN")

trevigiano.Trevigiano(plugins, model=model, token=token).run()
