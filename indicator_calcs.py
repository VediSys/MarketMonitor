# indicator_calcs.py |73
# logic expansion-oriented architecture
import numpy as np


def bb_calcs(
    curr_bb_up, curr_bb_mid, curr_bb_low,
    prev_bb_up, prev_bb_mid, prev_bb_low,
    last_bb_mid): #last_bb_up, , last_bb_low):
    """ bb calcs temp logicus:
    	if -3 >= -2 & -2 > -1; & vice versa."""
    if (last_bb_mid >=prev_bb_mid and prev_bb_mid >=curr_bb_mid):
    	bb_clr, bb_i = 'salmon','↓'
    elif (last_bb_mid <=prev_bb_mid and prev_bb_mid <curr_bb_mid):
        bb_clr, bb_i = 'aqua','↑'
    else: bb_clr, bb_i = 'lightgrey','≈'
    # -/^-.
    if prev_bb_up >=curr_bb_up:
    	bb_ih_clr, bb_ih = 'salmon','↓'
    elif prev_bb_up <curr_bb_up:
    	bb_ih_clr, bb_ih = 'aqua','↑'
    else: bb_ih_clr, bb_ih = 'lightgrey','≈'
    # -\v-.
    if prev_bb_low >=curr_bb_low:
        bb_il_clr, bb_il = 'salmon','↓'
    elif prev_bb_low <curr_bb_low:
        bb_il_clr, bb_il = 'aqua','↑'
    else: bb_il_clr, bb_il = 'lightgrey','≈'

    return (bb_clr, bb_i,
        bb_ih_clr, bb_ih,
        bb_il_clr, bb_il)


def laguerre_calcs(_df,laga,lagb,_curr,_prev):
	""" dual 'La Guerre' logic types"""
	b_clr, s_clr = 'aqua','salmon' #'orangered'
    # decision logic type A
	if ((laga[_curr] <=0.03 and laga[_prev] <=0.025)
	or ( laga[_curr] >=laga[_prev])):
	    laga_clr, laga_i = b_clr,'•↑BUY↑'
	else:
		laga_clr, laga_i = s_clr,'•↓SELL↓'
	# decision logic type B
	if ((laga[_curr] ==0.0 and laga[_prev] <=0.01)
	or ( lagb[_curr] ==0.0 and lagb[_prev] <=0.01)):
	    lagb_clr, lagb_i = b_clr,'↑BUY↑'
	else:
	    lagb_clr, lagb_i = s_clr,'↓SELL↓'

	return laga_clr, laga_i, lagb_clr, lagb_i


def priceline_calcs(
    curr_o,curr_c,prev_h,prev_c,
        curr_rsi_a,curr_rsi_b, DEC):
    """ temp calcs, priceline colours"""
    if curr_c >prev_c and curr_o >prev_h:
    	calc_clr='aqua'
    else: calc_clr='orange'
    # ---.
    if curr_o <=curr_c:
    	price_clr='lightskyblue'
    else: price_clr='salmon'
    # rsi priceline calc
    if curr_rsi_b <=curr_rsi_a:
    	d_g, price_clr=np.round(
    	    curr_rsi_a -curr_rsi_b,DEC),'hotpink'
    else: d_g, price_clr=np.round(
        curr_rsi_b -curr_rsi_a,DEC),'royalblue'

    return calc_clr, price_clr, d_g
