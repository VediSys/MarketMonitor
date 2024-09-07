# -*- coding: utf-8 -*- 24012023:
""" portfolio.py |58
    - yahoo format; 0306-0608,2024."""

def Portfolio(T, D, I):
	""" receives 35,14,16 (int 0-34, 0-13, 0-15).
	    returns (str, int, str). 17='BTC-CAD'"""
	symbol, days, interval = (['ADA-USD',
	    'AKT-USD','ATOM-USD','BTC-USD','DASH-USD','DOGE-USD',
	    'ETH-USD','EXRO.TO','HIVE.V','KAVA-USD','LPS.V',
	    'MKR-USD','OP-USD','SAND-USD','XLM-USD','WTI',
	    '^GDAXI','SOL-USD','BTC-CAD','WKHS','NDAQ',
	    'SNDL','FONE-USD','FM.TO','GC=F','SI=F',
	    'AUD=X','CAD=X','JPY=X','VET-USD','DGB-USD',
	    'USD','CDZI','CVS','PEPECOIN-USD'], [90,
	    1,2,3,5,7,10,20,30,45,60,
        90,120,180], ['1d',
        '1m','2m','5m','15m','30m',
        '60m','90m','1d','5d','1wk',
        '1mo','3mo','6mo','1yr','1y'])

	return symbol[T], days[D], interval[I]


def folio():
	""" for tkinter """
	# class def init():# T: 0-36, D: 0-13, I: 0-12
	ticker = ['BTC-USD', # default
	    'ADA-USD','AKT-USD','ATOM-USD',
	    'DASH-USD','DOGE-USD',
	    'ETH-USD','FIL-USD','HIVE.V',
	    'KAVA-USD','LPS.V',
	    'MKR-USD','OP-USD','SAND-USD',
	    'XLM-USD','WTI',
	    '^GDAXI','SOL-USD','BTC-CAD',
	    'WKHS','NDAQ',
	    'SNDL','FONE-USD','FM.TO',
	    'GC=F','SI=F',
	    'AUD=X','CAD=X','JPY=X',
	    'VET-USD','DGB-USD',
	    'USD','CDZI','CVS',
	    'ADA-USD','AXS-USD','PEPECOIN-USD']

	days = [90, # default
	    1, 2, 3, 5, 7,10,30,45,60,90,
	    120,180,240]

	interval = ['1d', # default
	    '1m','5m','15m','30m','60m',
	    '1h','1d','5d','1wk']
	# ---.
	t_len, d_len, i_len= (
	    len(ticker), len(days), len(interval))
	
	return (
	    ticker, days, interval,
	    t_len, d_len, i_len)
