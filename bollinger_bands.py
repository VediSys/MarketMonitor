# -*- coding: utf-8 -*- 24012023:
# bollinger_bands.py |68 updated to '[:]'
from __future__ import absolute_import
import numpy as np

from pyti import catch_errors
from pyti.function_helper import (
    fill_for_noncomputable_vals)

from pyti.simple_moving_average import (
    simple_moving_average as sma)
#from six import range


dev = 2 #1.618 #orig.:2.0


def upper_BB_band(data,period,std_mult=dev):
    """ Upper Formula:
            SMA(t) +STD( SMA(t -n:t)) *std_mult"""
    catch_errors.check_for_period_error(data, period)
    # ---.
    period    = int(period)
    simple_ma = sma(data, period)[period -1:]

    upper_bb = []
    for idx in range(len(data) -period +1):
        std_dev = np.std(
            data[idx:idx
            +period])
        upper_bb.append(
            simple_ma[idx]
            +std_dev
            *std_mult)

    upper_bb = fill_for_noncomputable_vals(
        data, upper_bb)

    return upper_bb[:]


def middle_BB_band(data, period):#, std=2.0):
    """ Middle Formula: sma()"""
    catch_errors.check_for_period_error(data, period)
    period = int(period)
    mid_bb = sma(data, period)

    return mid_bb[:]


def lower_BB_band(data, period, std=dev): #2.0):
    """ Lower Formula:
    	    SMA(t) -STD(SMA(t -n:t)) *std_mult"""
    catch_errors.check_for_period_error(data, period)
    period    = int(period)
    simple_ma = sma(data, period)[period -1:]

    lower_bb = []
    for idx in range(len(data) -period +1):
        std_dev = np.std(data[idx:idx +period])

        lower_bb.append(simple_ma[idx] -std_dev *std)

    lower_bb = fill_for_noncomputable_vals(
        data, lower_bb)

    return lower_bb[:]
