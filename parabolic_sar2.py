# -*- coding: utf-8 -*-#updated[:]
""" parabolic2.py |41✓ """
import numpy as np


def Parabolic(df_h, df_l,af, amax, df): #, dec):
    high, low = (df_h, df_l) #df['High'], df['Low']
    #high, low = (df['High'], df['Low'])
    sig0, xpt0, af0 = (True, high.iloc[0], af)
    sar = [low.iloc[0] -(high -low).std()]

    for i in np.arange(1, len(df_h)):
        sig1, xpt1, af01 = (sig0, xpt0, af0)
        lmin = min( low.iloc[i -1], low.iloc[i])
        lmax = max(high.iloc[i -1], high.iloc[i])
        # ---.
        if sig1:
            sig0 = low.iloc[i] >sar[-1]
            xpt0 = max(lmax, xpt1)
        else:
            sig0 = high.iloc[i] >=sar[-1]
            xpt0 = min(lmin, xpt1)
        # ---.
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
        # ---.
        sar.append(sari)
        #sar = round(sar,dec)

    return sar[:] #sar.append(sari)
