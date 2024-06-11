# External imports
import numpy as np
from typing import Any


def np_arange_with_end_limit(start: float, stop: float, step: float) -> np.ndarray[Any, Any]:
    '''Return a numpy array with the same behavior as np.arange, but with an inclusive stop limit.

    Withconventional np.arange:
    np.arange(start=3, stop=5, step=1) -> [3 4]

    With this function:
    np_arange_with_end_limit(start=3, stop=5, step=1) -> [3 4 5]'''

    return np.arange(start=start, stop=stop + step, step=step)
