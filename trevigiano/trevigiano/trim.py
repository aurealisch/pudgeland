import textwrap
import typing


def trim(text: typing.Text) -> typing.Text:
    """Description

    Parameters
    ----------
    text : typing.Text
        Description

    Returns
    -------
    typing.Text
        Description
    """
    return textwrap.dedent(text)
