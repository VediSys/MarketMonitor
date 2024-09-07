# -*- coding: utf-8 -*- Pydroid |41✓✓
""" autosize.py |61
    - rounded yahoo format.
    - req'd: decimal places integer,
      data pre-call portfolio parameters
      by/as (int,int,int).
"""

import datetime as dt
from dateutil.relativedelta import \
    relativedelta
import numpy as np
import yfinance as api # as yf


def auto_size(dec, p_f):
	""" resolve to formatted quote file."""
	d_t = dt.datetime.now()
	df1 = api.download(
	    tickers  = p_f[0], start = d_t - relativedelta(
	    days     = p_f[1]), end  = d_t,
	    interval = p_f[2], ignore_tz = True, prepost = False)

	d_f = round(df1.dropna(),dec)

	df1 = 0 # clear temp file.
	#d_f.to_csv(p_f[0]+p_f[2]+'.csv') #optional
	return d_f


def autosize_type2(dec, p_f):
    """ by period string, i.e.,'1yr'."""
    df2 = api.download(
        tickers  = p_f[0],
        period   = p_f[1],
        interval = p_f[2], ignore_tz = True, prepost = False)

    d_f = round(df2.dropna(),dec)

    df2 = 0 # clear temp file.
    #d_f.to_csv(p_f[0]+p_f[2]+'.csv')
    return d_f


def obtain_quote(_t, _d, _i, _dec):
	""" obtain feed quote """
	#pf = folio(_t, _d, _i) # request treated data file into .iloc[:]
	#df = autosize(DEC, pf)
	# ---.
	_df = api.download(tickers=_t,
	    start=dt.datetime.now()-relativedelta(days=_d),
	    end=dt.datetime.now(),
	    interval=str(_i),ignore_tz=True,prepost=False)
	#_df = _df[-_d:] # [-n:] limit file size
	_df = np.round(_df.dropna(),_dec) # smooth data
	df_o, df_h, df_l, df_c = (
	    _df['Open'].iloc[:],_df['High'].iloc[:],
	    _df['Low'].iloc[:],_df['Close'].iloc[:])
	#return df, pf
	return _df, df_o, df_h, df_l, df_c
