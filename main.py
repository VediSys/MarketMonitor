# -*- coding: utf-8 -*-!/usr/bin/env python3: Pydroid 3.9, Android 11+: 07012024:
""" main.py |<400 ✓

    - All-in-one template script to display
        candlestick chart with:
        Bollinger Bands, triple PSAR, dual RSI,
        Stochastic, MACD, WPR.
    - *required Pydroid installs for all modules:
        datetime, dateutil,
        matplotlib, mplfinance,
        numpy, pyti, six, tkinter, yfinance.
    ---------------------------------------------
    - 'mpl/mpf/tk' OLDER TEST REFERENCE+w/notes.
    - BOLLINGER PERIOD ERROR: 15072024
    - *note: ?-mtrla-octacore/a11 issue;
      Pydroid has a seemingly 9 indicator limit,
      even though the documentation allows for 32.
"""

import tkinter           as tk
import numpy             as np #import pandas as pd
import matplotlib.pyplot as plt
import mplfinance        as mpf

from autosize          import obtain_quote
from portfolio         import folio

from bollinger_bands   import (
    upper_BB_band  as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band  as bb_low)
from parabolic_sar2    import Parabolic #from intraday2 import price_diff
from macd_signal       import Macd
from relative_strength import Relative
from stochastic        import Stochastic
from williams_range    import WPR
# calcs
from indicator_calcs import \
    rsi_calcs, priceline_calcs
# theme
from themestyle import \
    Theme, Chart_Type, style_dict


FILENAME = "tk_EA_BMPRSW.py"
# tkinter window header item removal.
plt.rcParams['toolbar'] = 'toolmanager'
rpm = {
    0:'back',1:'forward',2:'help',3:'home',
    4:'pan',5:'save',6:'subplots',7:'zoom'}
# decimal places for calculations,
#    indicators and quote display.
DEC = 2
# set default quote range in portfolio.py!
Ticker,Days,Interval, T_len,D_len,I_len = folio()
CURR, PREV, LAST, PRIOR = -1, -2, -3, -D_len
# indicator parameters, periods.
af1, af2, af3, am1, am2, am3 = ( # triple PSAR
    0.01, 0.02, 0.05,
    0.1,  0.2,  0.5)
rsi_a_p, rsi_b_p =  8,  5    # dual RSI, default:14,8
bb_p, wpr_p      = 17, 14    # BB, WPR periods
fast, slow, ema  = 12, 26, 9 # MACD sa, ema periods
sto_a, sto_b     = 14,  3    # Stochastic periods


def exit_app():
	""" exit(), or: '...command=exit)'."""
	#root.update() # }
	root.destroy() # } method 1
	return #exit()   #   method 2


def clear_all():
    """ clear spinbox fields from/to."""
    spin1.delete(0,8) #0,END)
    spin2.delete(0,3) #0,END)
    spin3.delete(0,3) #0,END)
    root.destroy()  # }
    return


def select_0(*args): # *args req'd to animate; ignore error.
    """ load spinbox text into button text."""
    _df = []
    button1["background"] = 'khaki'
    button1["text"] = ("Click to view "
        +spin1.get()+", "
        +spin2.get()+" days, ["
        +spin3.get()+"] period.")
    button1.grid(row=2, column=0, columnspan=2)
    return


def tint_interpolations(rsia,rsib):
	""" ---."""
	fb_up, fb_dn = (
	    dict(y1=rsia,y2=rsib,where=(rsib<=rsia),
	        color="r",alpha=0.4,interpolate=True),
	    dict(y1=rsia,y2=rsib,where=(rsib>rsia),
	        color="b",alpha=0.8,interpolate=True))

	fb_up['panel'], fb_dn['panel'] = 1, 1

	return fb_up, fb_dn


"""def price_diff(_df):
    "" Intraday price change marker.""
    for index, row in _df.iterrows(): # ignore error.
        diff = (_df['Open'].iloc[row]
            -_df['Close'].iloc[row]
            )
        diff_pct = diff /_df['Open'].iloc[row]
        # ---.
        up_mark, dn_mark = [], [] #(), ()
        if diff_pct >= 0.05:
            up_mark.append(row['Close'])
            dn_mark.append(np.nan)
        elif diff_pct < -0.05:
            dn_mark.append(row['Close'])
            up_mark.append(np.nan)
        else:
            up_mark.append(np.nan)
            dn_mark.append(np.nan)
    return np.array(up_mark, dn_mark)"""


def main():
	""" obtain yahoo finance quotes via tkinter
	    spinbox and display custom template."""
	button1["background"] = 'lightgrey'
	
	_t, _d, _i = "",0,""

	_t, _d, _i = (
	    str(spin1.get()),
	    int(spin2.get()),
	    str(spin3.get()))

	_df, df_o, df_h, df_l, df_c = obtain_quote(
	    _t, _d, _i, DEC)

	curr_o, curr_c = (
	    df_o.iloc[CURR],
	    df_c.iloc[CURR])

	prev_h, prev_c = (
	    df_h.iloc[PREV],
	    df_c.iloc[PREV])

	prior_c = df_c.iloc[PRIOR]

	curr, prior, curr_str = (
	    _df.iloc[CURR],
	    _df.iloc[PRIOR],
	    str(df_c.iloc[CURR]))

	#two_points = [(prior_str, prior_c),(curr_str, curr_c)]

	# indicators #up_mark, dn_mark = price_diff(_df)
	# bb
	bb_u, bb_m, bb_l = (
	    bb_up( df_c,bb_p),
	    bb_mid(df_c,bb_p),
	    bb_low(df_c,bb_p))

	curr_bb_up, curr_bb_mid, curr_bb_low = (
	    np.round(bb_u[CURR],DEC),
	    np.round(bb_m[CURR],DEC),
	    np.round(bb_l[CURR],DEC))
	# psar
	sar1, sar2, sar3 = (
	    Parabolic(df_h,df_l,af1,am1,_df),
	    Parabolic(df_h,df_l,af2,am2,_df),
	    Parabolic(df_h,df_l,af3,am3,_df))

	curr_sar1, curr_sar2, curr_sar3 = (
	    np.round(sar1[CURR],DEC),
	    np.round(sar2[CURR],DEC),
	    np.round(sar3[CURR],DEC))
	# macd
	macd, signal, histogram = Macd(
	    df_c, fast, slow, ema)
	# rsi
	rsia, rsib = (
	    Relative(df_c,rsi_a_p,DEC),
	    Relative(df_c,rsi_b_p,DEC))

	curr_rsi_a, curr_rsi_b = (
	    np.round(rsia[CURR],DEC),
	    np.round(rsib[CURR],DEC))
	# wpr
	wpr = WPR(df_c, df_h, df_l, wpr_p)

	curr_wpr = np.round(wpr.iloc[CURR],DEC)
	# sto
	sto = Stochastic(_df, sto_a, sto_b)
	# ---.
	ind_color = ['royalblue','khaki','orangered',
	    'yellow','lime','w',
	    'r','c','dimgrey','r', #'maroon',
	    'chartreuse',
	    'forestgreen','darkolivegreen']
	# up, down marker panel
	#up_mark_panel, dn_mark_panel = ( # marker.0
    #    mpf.make_addplot(up_mark,color='orange',type='scatter',marker='v',markersize=100),
    #    mpf.make_addplot(dn_mark,color='lime',type='scatter',marker='^',markersize=100))
	bbu_panel, bbm_panel, bbl_panel = (
	    mpf.make_addplot(bb_u,color=ind_color[0],linestyle='-'),
	    mpf.make_addplot(bb_m,color=ind_color[1],linestyle='-'),
	    mpf.make_addplot(bb_l,color=ind_color[6],linestyle='-'))

	sar1_panel, sar2_panel, sar3_panel = (
	    mpf.make_addplot(sar1,color=ind_color[6],type='scatter'),
	    mpf.make_addplot(sar2,color=ind_color[1],type='scatter'),
	    mpf.make_addplot(sar3,color=ind_color[0],type='scatter'))
	# axes panels
	rsia_panel, rsib_panel = (
	    mpf.make_addplot(rsia,color=ind_color[2], #'orangered',
	        linestyle='-',panel=1,secondary_y=False),
	    mpf.make_addplot(rsib,color='dodgerblue',
	        linestyle='-',panel=1,secondary_y=False))
	#sto_panel = mpf.make_addplot(sto[['%K', '%D', '%SD', 'UL', 'DL']],
	#sto_k_panel = mpf.make_addplot(
	#    sto[['%K',]], color='grey',
	#    ylim=[0, 100], panel=1, secondary_y=False) #ylabel='Stoch')
	sto_h_panel = mpf.make_addplot(
	    #sto[['%K', 'UL', 'DL']],
	    sto[['UL']], color=ind_color[0], #'aqua',
	    ylim=[0, 100], panel=1, secondary_y=False) #ylabel='Stoch')

	sto_l_panel = mpf.make_addplot(
	    sto[['DL']], color=ind_color[2], #'orangered',
	    ylim=[0, 100], panel=1, secondary_y=False)
	# macd in panel 2
	macd_panel, signal_panel, histogram_panel = (
	    mpf.make_addplot(macd,color=ind_color[0],linestyle='-',panel=2,secondary_y=False),
	    mpf.make_addplot(signal,color=ind_color[6],linestyle='-',panel=2,secondary_y=False),
	    mpf.make_addplot(histogram,color=ind_color[8],type='bar',panel=2,secondary_y=False))
	# wpr in panel 3
	wpr_panel = mpf.make_addplot(wpr,color='c',linestyle='-',panel=2,secondary_y=False)
	# idc8r.: (14) as of mod_16012025
	indicators = [ #up_mark_panel, dn_mark_panel,
	    bbu_panel, bbm_panel, bbl_panel,
	    sar1_panel, sar2_panel, sar3_panel,
	    rsia_panel, rsib_panel,
	    sto_h_panel, sto_l_panel,
	    #sto_k_panel,
	    macd_panel, signal_panel, histogram_panel,
	    wpr_panel]
    # output_to_ax0[0]:'mpf'an'axes'to'plt' —————|
	c_vals, leg_fnt = {}, 19

	interpolations = tint_interpolations(rsia, rsib)

	calc_clr, price_clr, d_g = priceline_calcs(
	    curr_o, curr_c, prev_h, prev_c, curr_rsi_a, curr_rsi_b, DEC)

	dg_clr = rsi_calcs(curr_rsi_a, curr_rsi_b)
	# ———————————————————————————————————————————|
	fig0, ax0 = mpf.plot(_df,
	    #fill_between=interpolations,
	    style=mpf.make_mpf_style(base_mpf_style=Theme(3),
	        marketcolors=mpf.make_marketcolors(
	            up='dodgerblue', down='tomato',edge='dimgrey',
	            wick={'up':'w','down':'w'},volume='in', ohlc='in'),
	        gridcolor='dimgrey', facecolor='k', edgecolor='y',
	        rc=style_dict),
	    type=Chart_Type(3),
	    alines=[
	        (prior.name.date(), prior_c),
	        (curr.name.date(), curr_c)],
	    addplot=indicators,
	    hlines=dict(
	        hlines=[curr_c, prev_c],
	        colors=[price_clr, calc_clr],
	        linestyle='-.',linewidths=[2.2, 1.7],alpha=0.5),
	    panel_ratios=(5,2,1,1),
	    volume=True, volume_panel=3,
	    return_calculated_values=c_vals,
	    show_nontrading=False, #figratio =(12,8),
	    returnfig=True,
	    figscale=1.75, figsize=(10.3, 20.5))
	#test#ax0=fig0.add_axes([.05, .03, .9, .92])
	# remove window toolbar items
	for idx, item in enumerate(rpm, start=0):
		fig0.canvas.manager.toolmanager.remove_tool(
		    rpm[item])
	# window border top: last quote details
	fig0.canvas.manager.set_window_title(
	    '%s       %i days of %s [%s]  $%s' % (
	        curr.name.date().strftime('%A, %b.%e, %Y.'),
	        _d, _t, _i, curr_str))
	# figure border: last quote details
	#ax0[0].text(0.11, 0.95,
	#    str(_d)+' days of ['+_i+'] '+_t+' $'+curr_str,color=price_clr,fontsize=24)
    # chart right: trading density
	df_len, _y = (len(_df), -1)
	for _y in df_c:
	    ax0[0].annotate('          ' # 10 spaces
	        +str(_y), (df_len, _y),
	        transform=ax0[0].transAxes,
	        color="lime", alpha=0.25)
    # quote on priceline - redux'ed!
	ax0[0].annotate(str(_t)+'\n', #$'+curr_str,
	    (_d, curr_c),
	    fontsize=12, color='y', xytext=(_d, curr_c), alpha=0.7)
	# text on priceline in chart
	ax0[0].annotate(curr_str, (_d, curr_c),
        fontsize=14, color='khaki', #=price_clr,
        xytext=(_d, curr_c), alpha=1.0)
    # in-chart legend box
	ax0[0].annotate(
	    #f"{_d:} days {_t:}[{_i:}]" #\n ${curr_str:}"
	    #+f"\n{curr.name.date().strftime('%A,%b/%e/%Y'):}"
	    f"O: ${curr['Open']:.2f}\nH: ${curr['High']:.2f}"
	    +f"\nL: ${curr['Low']:.2f}\nC: ${curr_c:.2f}"
	    +f"\nV: {curr['Volume']:}",
	    #+f"\n\nBB  up ({ bb_p:}): {curr_bb_up:.2f}"
	    #+f"\nBBmid ({ bb_p:}): {curr_bb_mid:.2f}"
	    #+f"\nBB low ({ bb_p:}): {curr_bb_low:.2f}"
		#+f"\n\nSAR({  af1:}): {curr_sar1:.2f}"
		#+f"\nSAR({  af2:}): {curr_sar2:.2f}"
		#+f"\nSAR({  af3:}): {curr_sar3:.2f}",
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color='khaki', xytext=(0.01, 1.0), #0.62),
	    bbox=dict(boxstyle='square', fc=price_clr, alpha=0.19))
	rsi_height = 0.86 #orig:0.08
	ax0[0].annotate(
	    f"RSI ({rsi_b_p:}): {curr_rsi_b:}"
	    +f"\nRSI ({rsi_a_p:}): {curr_rsi_a:}\n", #+, \n
	    #"\n___≈±:", # {d_g:}",
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color='beige', xytext=(0.01, rsi_height),
	    bbox=dict(boxstyle='square', fc=price_clr, alpha=0.19))
	# rsi dg
	ax0[0].annotate(d_g,
	    xy=(len(_df),curr_c),textcoords='axes fraction',
	    fontsize=leg_fnt,color=dg_clr,xytext=(0.18,rsi_height))
	# williams
	ax0[0].annotate(
	    f"W% ({wpr_p:}): {curr_wpr:.2f}",
		xy=(len(_df), curr_c), textcoords='axes fraction',
	    fontsize=leg_fnt, color='c', xytext=(0.01, 0.01),
	    bbox=dict(boxstyle='square', fc=price_clr, alpha=0.19))
	# ---.
	button1["background"],button1["foreground"] = 'lightgrey','red'
	button1["text"] = 'repeat'

	plt.ion()
	plt.show()

	return


if __name__ == "__main__" : # DO NOT ALTER ——————|
    root = tk.Tk()
    root.configure(background='#505050')
    root.geometry('1000x250')
    root.title('Enter ticker, days, interval period')

    spin1, spin2, spin3 = (
        tk.Spinbox(root,from_=0,to=T_len,values=Ticker,width=9,font=("Helvetica 15"),
            textvariable=tk.StringVar(value=Ticker[0]),wrap=True),
        tk.Spinbox(root,from_=0,to=D_len,values=Days,width=4,font=("Helvetica 15"),
            textvariable=tk.IntVar(value=Days[0]),wrap=True),
        tk.Spinbox(root,from_=0,to=I_len,values=Interval,width=4,font=("Helvetica 15"),
            textvariable=tk.StringVar(value=Interval[0]),wrap=True))

    bg_clr, fg_clr = "lightgrey", "black"

    button0, button1, button2, button3 = (
        tk.Button(root,fg=fg_clr,bg=bg_clr,font=("Consolas 5"),
            text="Click to view selection",command=select_0),
        tk.Button(root,fg=fg_clr,bg=bg_clr,relief='raised',font=("Consolas 5"),
            text="",command=main),
        tk.Button(root,fg=fg_clr,bg=bg_clr,font=("Consolas 5"),
            text=" ∅ ",command=clear_all),
        tk.Button(root,fg=fg_clr,bg="coral",relief='raised',font=("Consolas 5"),
            text="Exit",command=exit_app)) #||command=exit))#window.destroy()))

    spin1.grid(row=0, column=0)
    spin2.grid(row=0, column=1)
    spin3.grid(row=0, column=2)

    button0.grid(row=1, column=0, columnspan=2)
    button1["background"],button1["foreground"] = bg_clr, fg_clr
    button2.grid(row=1, column=2)
    button3.grid(row=2, column=2)

    _t, _d, _i = "",0,""
    root.mainloop()
