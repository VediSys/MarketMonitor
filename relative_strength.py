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

"""
def Parabolic(df_h, df_l,af, amax): #dec,
    high, low = (df_h, df_l) #df['High'], df['Low']
    sig0, xpt0, af0 = (True, high[0], af)
    sar = [low[0] -(high -low).std()]

    for i in range(1, len(df_h)):
        sig1, xpt1, af01 = (sig0, xpt0, af0)
        lmin = min( low[i -1], low[i])
        lmax = max(high[i -1], high[i])
        #
        if sig1:
            sig0 = low[i] >sar[-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high[i] >=sar[-1]
            xpt0 = min(lmin, xpt1)
        #
        if sig0 == sig1:
            sari = sar[-1] +(xpt1 -sar[-1]) *af01
            af0 = min(amax, af01 +af)
            if sig0:
                af0 = af0 if xpt0 >xpt1 else af01
                sari = min(sari, lmin)
            else:
                af0 = af0 if xpt0 <xpt1 else af01
                sari = max(sari, lmax)
        else:
            af0 = af
            sari = xpt0
        #
        sar.append(sari)
        #sar = round(sar,dec)

    return sar"""
