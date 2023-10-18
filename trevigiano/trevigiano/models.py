from trevigiano import configurations, databases


class Model:

    def __init__(self, configuration: configurations.Configuration,
                 database: databases.Database) -> None:
        """Description

        Parameters
        ----------
        configuration : configurations.Configuration
            Description
        economics : economics.Economics
            Description
        """
        self.configuration = configuration
        self.database = database
