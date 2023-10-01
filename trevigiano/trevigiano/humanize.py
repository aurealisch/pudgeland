def humanize(number: int) -> str:
    return f"{number:,}".replace(",", "\u0020")
