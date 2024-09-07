# -*- coding: utf-8 -*- : Pydroid |35✓ #updated
""" commodity_channel.py
    """

from __future__ import absolute_import

import numpy as np
from pyti import \
    catch_errors
from pyti.typical_price import \
    typical_price
from pyti.simple_moving_average import \
    simple_moving_average as sma


def CCI(df_c, df_h, df_l, period):
    """ CCI.Formula: CCI = (TP - SMA(TP)) / (0.015 * Mean Deviation)"""
    catch_errors.check_for_input_len_diff(
        df_c, df_h, df_l)
    catch_errors.check_for_period_error(
        df_c, period)
    #dev = 0.015 #1.618,
    dev = 0.01618
    t_p = typical_price(
        df_c, df_h, df_l)
    cci = ((
        t_p -sma(t_p, period)) /
            dev *np.mean(
                np.absolute(
                    t_p -np.mean(t_p))
                )
        )

    return cci[:]
