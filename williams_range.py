#-*-utf-8-*-: Pydroid
""" williams_range.py |30✓
    - from www.prorealcode.com"""
from __future__ import absolute_import

import numpy as np
from pyti import catch_errors


#wpr_p = 14
#def WPR(df_c, df_h, df_l, period = wpr_p):
def WPR(df_c, df_h, df_l, period):
    """ hh = highest[period](df_h)
        ll = lowest[period](df_l)."""
    catch_errors.check_for_input_len_diff(
        df_c, df_h, df_l)
    catch_errors.check_for_period_error(
        df_c, period)

    h_h = np.sort(df_h) #, -1, 'stable', None) # period)
    l_l = np.sort(df_l) #, -1, 'stable', None) # period)
    wpr = (
        (h_h -df_c) #df_c[-1])
        /(h_h -l_l)) * -100

    return wpr
