"""
Defines functions for validating input dataframes
to the beer style prediction model
"""

from typing import Tuple

import pandas as pd

numerics = ['Size(L)',
            'OG',
            'FG',
            'ABV',
            'IBU',
            'Color',
            'BoilSize',
            'BoilTime',
            'Efficiency']

one_hots = ['SugarScale_Plato',
            'SugarScale_Specific Gravity',
            'BrewMethod_All Grain',
            'BrewMethod_BIAB',
            'BrewMethod_Partial Mash',
            'BrewMethod_extract']

def check_input(x: pd.DataFrame) -> Tuple[bool, str]:
    for feat in numerics:
        try:
            x[feat] = x[feat].astype(float)
            if x[feat].isnull().any():
                raise ValueError
        except ValueError:
            return False, f"Value for {feat} is non-numeric or Nan"
    for feat in one_hots:
        try:
            x[feat] = pd.to_numeric(x[feat])
            if x[feat].isnull().any() or \
               x.loc[(x[feat] != 0) & (x[feat] != 1), feat].any():
                raise ValueError
        except ValueError:
            return False, f"Value for {feat} is not 0 or 1"

    return True, "Input is ok."
