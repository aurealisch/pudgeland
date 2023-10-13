from trevigiano import configurations, databases


class Model:

    def __init__(self, configuration: configurations.Configuration,
                 database: databases.Database) -> None:
        self.configuration = configuration
        self.database = database
