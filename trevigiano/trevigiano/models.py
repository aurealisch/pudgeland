from trevigiano import configurations, economics


class Model:

    def __init__(self, configuration: configurations.Configuration,
                 economics: economics.Economics) -> None:
        """Description

        Parameters
        ----------
        configuration : configurations.Configuration
            Description
        economics : economics.Economics
            Description
        """
        self.configuration = configuration
        self.economics = economics
