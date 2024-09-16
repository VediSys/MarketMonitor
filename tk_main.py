#-*-utf-8-*-: Pydroid: tkinter ****reference version
""" tk_main is:
    tk_EA_BCLMPRW.py |393, №.3/5 base_arch 29072024. (++!)
*23122023, last edit: 03082024: w/notes on further development

    - All-in-one Pydroid periodic market monitor
      script using the yfinance API with
      custom indicators, data acquisition,
      portfolio and theme scripts.

    - displays window of axes in figure with:
      Bollinger Bands, dual LaGuerre,
      triple Parabolic Stop And Reverse,
      dual Relative Strength Index, Volume.
_________________________________________________.
@github/vedisys ©2024 ARR
coffee?;send BTC: 3MZm5HF7USTC1RcNk2pTduHoZ6oBdw9pUs
"""

# req'd (in sequence)
import tkinter as tk
import numpy   as np
import matplotlib.pyplot as plt
import mplfinance as mpf
# custom scripts (11)
from autosize  import obtain_quote
from portfolio import folio
# main panel indicators
#from intraday_pricechange import price_diff
from bollinger_bands import (
    upper_BB_band  as bb_up,
    middle_BB_band as bb_mid,
    lower_BB_band  as bb_low)
from parabolic_sar2    import Parabolic
# subplot panel indicators sequence
from laguerre          import LaGuerre
from relative_strength import Relative
from macd_signal       import Macd
from commodity_channel import CCI #*-
from williams_range    import WPR
# decisi logicum plurare, prix
from indicator_calcs  import \
    bb_calcs, laguerre_calcs, priceline_calcs
# output style
from themestyle import \
    Theme, Chart_Type, style_dict


FILENAME = "tk_EA_B3L2P3R2.py"
plt.rcParams['toolbar'] = 'toolmanager'

# class def init():# T: 0-35, D: 0-13, I: 0-12
#Ticker, Days, Interval, T_len, D_len, I_len = folio()

# window header default items
rpm = {0:'back',
    1:'forward',2:'help',3:'home',4:'pan',5:'save',
    6:'subplots',7:'zoom'} #List,Show show

# colours (0-12); in specific idx order!
i_clr = ['dodgerblue', #,'lime' -g maroon
	'khaki','orangered','dodgerblue','khaki','orangered',
	'dodgerblue','plum','dodgerblue','orangered','khaki',
	'chartreuse','c','orangered','darkslategrey','white']
F_CLR = '#505050' #i_clr[13]

# application, indicator parameters.
DEC = 2                       # default: 4
GAMMA, THETA = 0.25, 0.75     # default: 0.75
CURR, PREV, LAST = -1, -2, -3 # sets flow
# default: BB: 20, RSI: 14, 8, WPR: 14
bb_p, rsia_p, rsib_p, wpr_p = 17, 5, 8,14
fast,  slow,  ema  = 12,26, 9
fast2, slow2, ema2 = 11,17, 5
#up_mark, dn_mark = [],[]
af1, af2, af3, am1, am2, am3 = ( # Parabolic SAR
    0.01, 0.02, 0.05,            # default: ...0.03,
    0.1,  0.2,  0.5)             # default: ...0.3)
ccia_p, ccib_p = 17,23           # dual CCI (a,b)
CCI_RND = 10000000               # cci rounding factor


def exit_app():
	""" exit app"""
	return window.destroy()


def clear_all():
    """ clear spinbox fields from/to"""
    spin1.delete(0,8) #: 0,END)
    spin2.delete(0,3) #: 0,END)
    spin3.delete(0,3) #: 0,END)

    return


def select_0(*args): # req'd to animate; ignore Pydroid error
    """ load spinbox text into button text"""
    button1["background"] = i_clr[1]
    button1["text"] = ("Click to view "
        +spin1.get()+", "
        +spin2.get()+" days, ["
        +spin3.get()+"] period.")
    button1.grid(row=2, column=0, columnspan=2)

    return


"""def price_diff(_df): #, period=pf[2]):
    #"" Intraday price change marker.""
    up_mark, dn_mark = [],[]
    for idx, row in _df.iterrows(): #for row in _df.iterrows():
        diff = _df['Open'].iloc[row] -_df['Close'].iloc[row]
        diff_pct = diff /_df['Open'].iloc[row]
        if diff_pct > 0.05:
            up_mark.append(row['Close'])
            dn_mark.append(np.nan)
        elif diff_pct < -0.05:
            dn_mark.append(row['Close'])
            up_mark.append(np.nan)
        else:
            up_mark.append(np.nan)
            dn_mark.append(np.nan)
    return np.array(up_mark, dn_mark)""
""def save_png(_df, _t, _i):
    "" ---.""
    #_T, _I = (str(spin1.get()), str(spin3.get()))
    fig, _ax = mpf.plot(_df,
	    savefig=FILENAME+_t+'_'+_i+'.png')
    return None""********************* """


def tint_interpolations( #laga,lagb,
    rsia,rsib,ccia,ccib,macd,signal):
	ftint = ['royalblue','coral','cyan','lightblue','teal','salmon']
	#fb_up1, fb_dn1 = ( # interpolated laguerre: panel 1
	#    dict(y1=laga,y2=lagb,
	#        where=lagb<=laga,color="#e06666",alpha=0.4,interpolate=True),
	#    dict(y1=laga,y2=lagb,
	#        where=lagb >laga,color="#93c47d",alpha=0.4,interpolate=True))
	#fb_up1['panel'], fb_dn1['panel'] = 1, 1
	# rsiA, rsiB in panel 2
	fb_up2, fb_dn2 = (
	    dict(y1=rsia,y2=rsib,where=rsib<=rsia,color="#93c47d",alpha=0.4,interpolate=True),
	    dict(y1=rsia,y2=rsib,where=rsib >rsia,color="#e06666",alpha=0.4,interpolate=True))
	fb_up2['panel'], fb_dn2['panel'] = 2, 2
	# cciA, cciB in panel 4
	fb_up4, fb_dn4 = (
	    dict(y1=ccia,y2=ccib,where=ccib<=ccia,color=ftint[0],alpha=0.5,interpolate=True),
	    dict(y1=ccia,y2=ccib,where=ccib >ccia,color=ftint[1],alpha=0.5,interpolate=True))
	fb_up4['panel'], fb_dn4['panel'] = 4, 4
	# macd in panel 5
	fb_up5, fb_dn5 = (
	    dict(y1=macd.values,y2=signal.values,
	        where=signal<=macd,color="#93c47d",alpha=0.5,interpolate=True),
	    dict(y1=macd.values,y2=signal.values,
	        where=signal >macd,color="#e06666",alpha=0.5,interpolate=True))
	fb_up5['panel'], fb_dn5['panel'] = 5, 5

	return [ #fb_up1, fb_dn1,
	    fb_up2, fb_dn2,
	    fb_up4, fb_dn4, fb_up5, fb_dn5]


def main():
	""" ---."""
	button1["background"] = 'lightgrey'
	# reset parameters, obtain file via tkinter
	_t, _d, _i = "",0,""
	_t, _d, _i = str(spin1.get()),int(spin2.get()),str(spin3.get())
	# obtain OHLC feed quotes
	_df, df_o, df_h, df_l, df_c = obtain_quote(_t, _d, _i, DEC)
	_tail = str(_df.tail(3)) # extract last 3 file records
	# alias to simplify logic modifications
	curr_rec, curr_str = _df.iloc[CURR],str(df_c.iloc[CURR])
	curr_o, curr_c = df_o.iloc[CURR],df_c.iloc[CURR]
	prev_h, prev_c = df_h.iloc[PREV],df_c.iloc[PREV]
	#-u-last_c = df_c.iloc[LAST] #last_o, last_c = df_o.iloc[LAST],
	# ---.
	#def indications():
	#up_mark, dn_mark = price_diff(_df)
	# main panel 0: bb
	bb_u, bb_m, bb_l = (bb_up(df_c,bb_p),bb_mid(df_c,bb_p),bb_low(df_c,bb_p))
	curr_bb_up, curr_bb_mid, curr_bb_low = (
	    np.round(bb_u[CURR],DEC),np.round(bb_m[CURR],DEC),np.round(bb_l[CURR],DEC))
	prev_bb_up, prev_bb_mid, prev_bb_low = (
	    np.round(bb_u[PREV],DEC),np.round(bb_m[PREV],DEC),np.round(bb_l[PREV],DEC))
	#last_bb_up, last_bb_mid, last_bb_low = (
	#    np.round(bb_u[LAST],DEC),np.round(bb_m[LAST],DEC),np.round(bb_l[LAST],DEC))
	last_bb_mid = np.round(bb_m[LAST])
	# Bollinger calcs
	bb_clr,bb_i,bb_ih_clr,bb_ih,bb_il_clr,bb_il = bb_calcs(
	    curr_bb_up, curr_bb_mid, curr_bb_low,
	    prev_bb_up, prev_bb_mid, prev_bb_low,
	    last_bb_mid) #last_bb_up, , last_bb_low)
	# psar 0
	sar1, sar2, sar3 = (Parabolic(df_h,df_l,af1,am1,_df),
	    Parabolic(df_h,df_l,af2,am2,_df),Parabolic(df_h,df_l,af3,am3,_df))
	curr_sar1, curr_sar2, curr_sar3 = (
	    np.round(sar1[CURR],DEC),np.round(sar2[CURR],DEC),np.round(sar3[CURR],DEC))
	# lag 1
	laga, lagb = LaGuerre(_df,GAMMA),LaGuerre(_df,THETA)
	curr_laga, curr_lagb = np.round(laga[CURR],DEC),np.round(lagb[CURR],DEC)
	# 'La Guerre' calcs
	laga_clr, laga_i, lagb_clr, lagb_i = laguerre_calcs(_df,laga,lagb,CURR,PREV)
	# rsi 2
	rsia, rsib = Relative(df_c,rsia_p,DEC),Relative(df_c,rsib_p,DEC)
	curr_rsi_a, curr_rsi_b = np.round(rsia[CURR],DEC),np.round(rsib[CURR],DEC)
	# williams % range 3
	wpr = WPR(df_c, df_h, df_l, wpr_p)
	curr_wpr = np.round(wpr.iloc[CURR],DEC)
	# subpanel 4: cci
	ccia, ccib = CCI(df_c,df_h,df_l,ccia_p),CCI(df_c,df_h,df_l,ccib_p)
	curr_cci_a, curr_cci_b = np.round(ccia[CURR]/CCI_RND,DEC),np.round(ccib[CURR]/CCI_RND,DEC)
	# subpanel 5: macd
	macd, signal, histogram = Macd(df_c,fast,slow,ema)
	# panels
	#up_mark_panel, dn_mark_panel = (
	#    mpf.make_addplot(up_mark,color='orange',type='scatter',marker='v',markersize=100),
	#    mpf.make_addplot(dn_mark,color='lime',type='scatter',marker='^',markersize=100))
	bbu_panel, bbm_panel, bbl_panel = (
	    mpf.make_addplot(bb_u,color=i_clr[0],linestyle='-'), #orig: '-'
	    mpf.make_addplot(bb_m,color=i_clr[1],linestyle='-'), #orig: ':'
	    mpf.make_addplot(bb_l,color=i_clr[2],linestyle='-'))
	sar1_panel, sar2_panel, sar3_panel = (
	    mpf.make_addplot(sar1,color=i_clr[3],type='scatter'),
	    mpf.make_addplot(sar2,color=i_clr[4],type='scatter'),
	    mpf.make_addplot(sar3,color=i_clr[5],type='scatter'))
	laga_panel, lagb_panel = (
	    mpf.make_addplot(laga,color=i_clr[6],linestyle='-',panel=1,secondary_y=True),
	    mpf.make_addplot(lagb,color=i_clr[7],linestyle='-',panel=1,secondary_y=True))
	rsia_panel, rsib_panel = (
	    mpf.make_addplot(rsia,color=i_clr[8],linestyle='-',panel=2,secondary_y=False),
	    mpf.make_addplot(rsib,color=i_clr[9],linestyle='-',panel=2,secondary_y=False))
	wpr_panel = mpf.make_addplot(wpr,color=i_clr[11],linestyle='-',panel=3,secondary_y=False)
	ccia_panel, ccib_panel = (
	    mpf.make_addplot(ccia,color=i_clr[12],linestyle='-',panel=4,secondary_y=False),
	    mpf.make_addplot(ccib,color=i_clr[13],linestyle='-',panel=4,secondary_y=False))
	histogram_panel, macd_panel, signal_panel = (
	    mpf.make_addplot(histogram,
	        color=i_clr[1],panel=5,type='bar',width=0.5,alpha=0.6,secondary_y=True),
	    mpf.make_addplot(macd,color=i_clr[0],panel=5,secondary_y=False),
	    mpf.make_addplot(signal,color=i_clr[2],panel=5,secondary_y=False))
	# pool panels for mplfinance figure
	indicators = [ #up_mark_panel, dn_mark_panel,
	    bbu_panel, bbm_panel, bbl_panel,
	    sar1_panel,sar2_panel,sar3_panel,
	    laga_panel, lagb_panel,
	    rsia_panel, rsib_panel,
	    wpr_panel, ccia_panel, ccib_panel,
	    histogram_panel, signal_panel, macd_panel
	    ]
    # def output_to_ax_0()-------------------------|
	interpolations = tint_interpolations(
	    rsia,rsib,ccia,ccib,macd,signal)
	calc_clr, price_clr, d_g = priceline_calcs(
	    curr_o,curr_c,prev_h,prev_c,
	        curr_rsi_a,curr_rsi_b,DEC)
	c_vals, leg_fnt = {}, 19
	# figure values
	fig, _ax = mpf.plot(_df,fill_between=interpolations,
	    style=mpf.make_mpf_style(base_mpf_style=Theme(3),
	        marketcolors=mpf.make_marketcolors(up='dodgerblue',down='tomato',edge='w',
	            wick={'up':'w','down':'w'},volume='in',ohlc='in'),
	        gridcolor='dimgrey', facecolor='k', edgecolor='y', rc=style_dict),
	    type=Chart_Type(3), addplot=indicators,
	    hlines=dict(hlines=[curr_c, prev_c],colors=[price_clr, calc_clr],
	        linestyle='-.',linewidths=[2.2, 1.7],alpha=0.4),
	    xlabel=(
	        '•'+FILENAME+'•\n'+_t+' $'+str(curr_c)+'\n'+_tail),
	    panel_ratios=( 4, 1, 1, 1, 1, 1), volume=True,volume_panel=1, #<--!
	    return_calculated_values=c_vals,show_nontrading=False,
	    figratio=(12, 8),returnfig=True,figscale=1.75,figsize=(10.3, 20.5))
	# remove window toolbar items; ignore 'item' error
	for idx, item in enumerate(rpm, start=0):
		fig.canvas.manager.toolmanager.remove_tool(
		    rpm[item])
	# last quote details in window border
	fig.canvas.manager.set_window_title(
	    '%s    %i days of %s [%s]    $%s' % ( #FILENAME, #||
	        curr_rec.name.date().strftime('%A, %b. %e/%Y'),
	        _d, _t, _i, curr_str))
	# axes values
	#_ax[0].grid(False) # remove ax0 grid
	# trading density in chart right
	df_len, _y = len(_df), -1
	for _y in df_c:
	    _ax[0].annotate('          '+str(_y),(df_len, _y),transform=_ax[0].transAxes,
	        fontsize=10,color=i_clr[11],alpha=0.25)
    # current quote on priceline in chart
	_ax[0].annotate(str(_t)+'\n'+curr_str,(_d, curr_c),
	    fontsize=10,color=i_clr[15],xytext=(_d, curr_c),alpha=0.7)
    # (-)current date), ohlc in chart
	_ax[0].annotate( #f"{_d:} day(s) {_t:} [{_i:}]"
        #+f"\n{curr_rec.name.date().strftime('%A, %b/%e/%Y'):}"
	    f"\nO: ${_df['Open'].iloc[CURR]:.2f}\nH: ${_df['High'].iloc[CURR]:.2f}" #(-) +f"\n
	    +f"\nL: ${_df['Low'].iloc[CURR]:.2f}\nC: ${_df['Close'].iloc[CURR]:.2f}\n", #<<==!!
		xy=(len(_df), curr_c),textcoords='axes fraction',
	    fontsize=leg_fnt,color=i_clr[1],xytext=(0.01, 1.0)) #,alpha=0.85)
	# bb decision logic
	_ax[0].annotate(bb_ih+"|",
		xy=(len(_df), curr_c),textcoords='axes fraction',
	    fontsize=leg_fnt,color=bb_ih_clr,xytext=(0.01, 0.96)) #,alpha=0.85)
	_ax[0].annotate(bb_i+"|",
		xy=(len(_df), curr_c),textcoords='axes fraction',
	    fontsize=leg_fnt,color=bb_clr,xytext=(0.01, 0.90)) #,alpha=0.85)
	_ax[0].annotate(bb_il+"|",
		xy=(len(_df), curr_c),textcoords='axes fraction',
	    fontsize=leg_fnt,color=bb_il_clr,xytext=(0.01, 0.84)) #,alpha=0.85)
    # laguerre decision logic type A
	_ax[0].annotate(laga_i,xy=(len(_df),curr_c),textcoords='axes fraction',
	    fontsize=24,color=laga_clr,xytext=(0.04,0.04))
	# laguerre decision logic type B <--logic error
	_ax[0].annotate(lagb_i,xy=(len(_df),curr_c),textcoords='axes fraction',
	    fontsize=22,color=lagb_clr,xytext=(0.24,0.04))
	# subpanel annotations (0-13), *13 based on 6 indicators
	legend_array = (
	    f"- BB  up ({ bb_p:}): {curr_bb_up:.2f}",
	    f"- BBmid ({ bb_p:}): {curr_bb_mid:.2f}",
	    f"- BB low ({ bb_p:}): {curr_bb_low:.2f}",
	    f"• psar({af3:}): {curr_sar3:.2f}",
	    f"• psar({af2:}): {curr_sar2:.2f}",
	    f"• psar({af1:}): {curr_sar1:.2f}",
	    f"- LaG A({GAMMA:}): {curr_laga*100:.2f}",
	    f"- LaG B({THETA:}): {curr_lagb*100:.2f}",
	    f"- RSI({rsia_p:}): {curr_rsi_a:}",
	    f"- RSI({rsib_p:}): {curr_rsi_b:}",
	    f"________±{d_g:}",
	    f"- WPR({wpr_p:}): {curr_wpr/10:.2f}",
	    f"- CCI({ccia_p:}): {curr_cci_a:.2f}",
	    f"- CCI({ccib_p:}): {curr_cci_b:.2f}")
	xy_txt = (0.96,
	    0.90,0.84,0.77,0.71,0.65,
	    0.58,0.52,0.45,0.39,0.33,
	    0.26,0.19,0.13) #,0.07,0.0)
	for idx, item in enumerate(xy_txt, start=0):
		_ax[0].annotate(
		    legend_array[idx],
		    xy=(len(xy_txt), curr_c),textcoords='axes fraction',
		    fontsize=leg_fnt,color=i_clr[idx],
		    xytext=(0.05, xy_txt[idx]), #!:indented
		    bbox=dict(boxstyle='square',fc='k',alpha=0.55))
	# -- _ax[2].text(xline=('.'),)
    # prep tk buttons
	button1["background"], button1["foreground"] = ('lightgrey','blue')
	button1["text"] = 'repeat'
	# ---.
	plt.ion()  # non-blocking window
	plt.show() # run GUI

	return


if __name__ == "__main__" : # main dialogue window
    window = tk.Tk()
    window.configure(background='darkslategrey',border=0) #'#969798',border=0)
    #window.overrideredirect(True) # revert to borderless window
    window.geometry('1000x250')
    window.title('Enter ticker, days, interval for Bollinger, LaGuerre, PSAR, RSI, Vol')
    # spinbox selection parameters
    Ticker, Days, Interval, T_len, D_len, I_len = folio()
    spin1, spin2, spin3 = (
        tk.Spinbox(window,from_=0,to=T_len,values=Ticker,width=9,font=("Helvetica 15"),
            textvariable=tk.StringVar(value=Ticker[0]),wrap=True),
        tk.Spinbox(window,from_=0,to=D_len,values=Days,width=4,font=("Helvetica 15"),
            textvariable=tk.IntVar(value=Days[0]),wrap=True),
        tk.Spinbox(window,from_=0,to=I_len,values=Interval,width=4,font=("Helvetica 15"),
            textvariable=tk.StringVar(value=Interval[0]),wrap=True))
    # button colors, parameters and actions
    fg_clr, bg_clr= "black", "lightgrey"
    button0, button1, button2, button3 = (
        tk.Button(window,fg=fg_clr,bg=bg_clr,font=("Consolas 5"),
            text="Click to view selection",command=select_0),
        tk.Button(window,fg=fg_clr,bg=bg_clr,relief='raised',font=("Consolas 5"),
            text="",command=main),
        tk.Button(window,fg=fg_clr,bg=bg_clr,font=("Consolas 5"),
            text=" ∅ ",command=clear_all),
        tk.Button(window,fg=fg_clr,bg="coral",relief='raised',font=("Consolas 5"),
            text="Exit",command=exit_app)) #command=exit))#window.destroy())
    #button4 = tk.Button(window,fg=fg_clr,bg="coral",relief=tk.RAISED,font=("Consolas 5"),
    #    text="Save", command=save_png)
    # widgets placement
    spin1.grid(  row=0, column=0)
    spin2.grid(  row=0, column=1)
    spin3.grid(  row=0, column=2)
    button0.grid(row=1, column=0, columnspan=2)
    button1["background"], button1["foreground"] = bg_clr, fg_clr
    button2.grid(row=1, column=2)
    button3.grid(row=2, column=2)
    # ---.
    _t, _d, _i = "",0,"" # 2nd reset input parms
    window.mainloop()    # run 'tkinter' dialogue GUI
