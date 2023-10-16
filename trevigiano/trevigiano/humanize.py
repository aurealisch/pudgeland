def humanize(number: int) -> str:
    """Description

    Parameters
    ----------
    number : int
        Description
    
    Returns
    -------
    str
        Description
    """
    return f'{number:,}'.replace(',', '\u0020')
