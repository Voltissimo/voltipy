import string
from typing import Union


def convert_notation(param: Union[str, tuple]) -> Union[str, tuple]:
    """
    Convert chess notation to nested list indexing
    :param param: chess notation string OR tuple
    :return: tuple of coords (row, col) OR chess notation string

    >>> convert_notation('a1')
    (0, 0)
    >>> convert_notation('e4')
    (4, 3)
    """
    assert len(param) == 2
    if type(param) is str:
        return (
            int(param[1]) - 1,
            string.ascii_lowercase.index(param[0])
        )
    elif type(param) is tuple:
        return f"{string.ascii_lowercase[param[1]]}{str(param[0] + 1)}"
