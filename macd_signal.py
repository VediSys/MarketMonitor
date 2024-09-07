#-*-utf-8-*-: Pydroid
""" macd_signal.py |15 ✓ #updated"""


def Macd(df_c, fast, slow, ema):
	""" MACD as an external function."""
	expa = df_c.ewm(span=fast, adjust=False).mean()
	expb = df_c.ewm(span=slow, adjust=False).mean()
	macd = expa -expb
	# ---.
	signal = macd.ewm(span=ema, adjust=False).mean()
	histogram = macd -signal

	return (macd[:], signal[:], histogram[:])
