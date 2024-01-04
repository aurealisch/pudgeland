class Error(Exception):
    pass

NotEnoughBananaError = Error("Недостаточно бананов")
NotEnoughCoinError = Error("Недостаточно монет")
