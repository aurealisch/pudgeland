import typing


class Configuration(typing.TypedDict):
    collectingRngStart: int
    collectingRngStop: int
    domesticationRatio: int
    purchaseCoin: int
    purchaseDiamond: int
    purchaseNetherite: int
