from trevigiano import configurations, economics


class Model:

    def __init__(self, configuration: configurations.Configuration,
                 economics: economics.Economics) -> None:
        self.configuration = configuration
        self.economics = economics
