import math

import numpy as np
import pandas as pd


def calculate_vpd(temp, rh):
    if pd.isna(temp) or pd.isna(rh):
        return np.nan
    es = 0.6108 * math.exp(17.27 * temp / (237.3 + temp))
    e = es * rh / 100
    vpd = es - e
    return vpd
