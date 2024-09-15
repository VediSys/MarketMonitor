# -*- coding: utf-8 -*-#updated
""" relative_strength.py |69 ""
	# rsi.
	rsiA = Rsi(df_c, rsiA_p, DEC)
	rsiB = Rsi(df_c, rsiB_p, DEC)
"""
import numpy as np


def Relative(prix, n, DEC): # in-house function.
    """ opt.: set RSI to: [14,{ 8], 7}."""
    deltas = np.diff(prix)
    seed = deltas[:n +1]
    up = seed[seed >=0].sum() /n
    dn = -seed[seed <0].sum() /n
    r_s = up /dn
    rsi = np.zeros_like(prix)
    rsi[:n] = 100. -100. /(1. +r_s)
    for q in range(n, len(prix)):
        delta = deltas[q -1]
        if delta >0:
            upval = delta
            dnval = 0.
        else:
            upval = 0.
            dnval = -delta
        up = (up *(n -1) +upval) /n
        dn = (dn *(n -1) +dnval) /n
        r_s = up /dn
        rsi[q] = 100. -100. /(1. +r_s)
        #rsi.append(rsi)
    return rsi[:]
