import os
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
sns.set_style("darkgrid")

import pandas as pd
from datetime import datetime,timedelta


#os.chdir('Python')
from eda_functions import *
from utilities import *
#os.chdir('../')

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#--------- Gain better -----------------------

def gain_better(
        data, 
        elo_diff = 0, 
        rank_diff = 0, 
        threshold = None, 
        tax = 0.0, 
        round_ = None, 
        limit = 200, 
        verbose=1, 
        data_back = 0,
        rst_idx = 1):
    '''
    Gives back the avarage performace of betting. Staight betting on the 
        player with the better elo-score AND the better Rank.
    
    data: the given DataFrame.
    
    tax: tax rate to be considered directly on the wager.
    
    round_: index of list. selecting the round to be inspected. If None then 
        all rounds are considered.
        ['1st Round', '2nd Round','3rd Round', '4th Round', 'Quarterfinals', 
        'Semifinals', 'The Final']
        
    limit: maximum odds to be considered
    
    thr: minimum odd as theshold for betting. If 'None' then threshold 
        calculated by tax if set.
        
    diff_elo: how much higher should the elo-score at least be.
    diff_rank: how much higher should the rank at least be
    verbose: if verbose is 1 summary is printed out
    
    
    data_back: if 1 a dataframe with the affected matches will be returned 
        including the rolling gain.
        
    rst_idx: if 1 the index of the returned dataframe is reset. 
        Else the indices remain as in the initial given data 
        (only needed if data_back = 1)
    '''
    
    # calculate the thershold according the tax if no threshold is given. 
    # Will be 1.0 id tax is 0.0
    thr = 1/(1-tax) if threshold == None else threshold
    
    rounds = pd.Series(['1st Round', '2nd Round','3rd Round', '4th Round', 
                        'Quarterfinals', 'Semifinals', 'The Final'])
    
    round_x = None if round_ == None else list([round_]) \
        if type(round_) == int else round_
    
    rnd = list(rounds) if round_x == None else list(rounds[round_x])
    
    dat = data[(data.Round.isin(rnd))]

    elo = elo_diff
    rk = rank_diff
    
    # selecting won bets 
    won = dat[(dat.elo_diff > elo) & (dat.rank_diff > rk) & \
              (dat.B365W >= thr) & (dat.B365W <= limit)]
    
    # amount of failed bets            
    lost = dat[(dat.elo_diff < -elo) & (dat.rank_diff < -rk) & \
               (dat.B365L >= thr) & (dat.B365L <= limit)]
    
    # How much got back
    cashback = won.B365W.sum()
    
    # invested
    invest = won.shape[0] + lost.shape[0]
    
    # ROI absolute
    gain = cashback - invest
    
    # ROI percentage
    ROI_perc = round((cashback/invest)*100,2)
    
    # ROI performance
    ROI_perf = round((gain/invest)*100,2)
    
    results = [invest, ROI_perf, gain]
    
    if verbose:
        print(f'Investment:         {invest}     (Number of matches)')
        print(f'Amount of return:   {round(cashback,2)}')
        print(f'Gain:               {round(gain,2)}')
        print(f'Percentage of ROI:  {ROI_perc} %')
        print(f'Performance of ROI: {ROI_perf} %')
    
    if data_back:
        won['gain'] = won.B365W - 1
        lost['gain'] = -1
        result_df = pd.concat([won, lost])
        result_df.sort_values(by=['Date'], inplace=True, ascending=True)
        result_df['rolling_gain'] = result_df.gain.cumsum()
        
        if rst_idx:
            #result_df.reset_index(drop=True)
            result_df.reset_index(inplace=True)
    
        return result_df
    else:
        return results
    
    

    
def gain_crossover(
        data, 
        elo_diff = 0, 
        rank_diff = 0, 
        threshold = None, 
        tax = 0.0, 
        round_ = None, 
        limit = 200, 
        verbose=1, 
        data_back = 0,
        rst_idx = 1):
    '''
    Gives back the avarage performace of betting. Staight betting on the 
        player with the better elo-score AND the better Rank.
    
    data: the given DataFrame.
    
    tax: tax rate to be considered directly on the wager.
    
    round_: index of list. selecting the round to be inspected. If None then 
        all rounds are considered.
        ['1st Round', '2nd Round','3rd Round', '4th Round', 'Quarterfinals', 
        'Semifinals', 'The Final']
        
    limit: maximum odds to be considered
    
    thr: minimum odd as theshold for betting. If 'None' then threshold 
        calculated by tax if set.
        
    diff_elo: how much higher should the elo-score at least be.
    diff_rank: how much higher should the rank at least be
    verbose: if verbose is 1 summary is printed out
    
    
    data_back: if 1 a dataframe with the affected matches will be returned 
        including the rolling gain.
        
    rst_idx: if 1 the index of the returned dataframe is reset. 
        Else the indices remain as in the initial given data 
        (only needed if data_back = 1)
    '''
    
    # calculate the thershold according the tax if no threshold is given. 
    # Will be 1.0 id tax is 0.0
    thr = 1/(1-tax) if threshold == None else threshold
    
    rounds = pd.Series(['1st Round', '2nd Round','3rd Round', '4th Round', 
                        'Quarterfinals', 'Semifinals', 'The Final'])
    
    round_x = None if round_ == None else list([round_]) \
        if type(round_) == int else round_
    
    rnd = list(rounds) if round_x == None else list(rounds[round_x])
    
    dat = data[(data.Round.isin(rnd))]

    elo = elo_diff
    rk = rank_diff
    
    # selecting won bets 
    won = dat[(dat.elo_diff < -elo) & (dat.rank_diff > rk) & \
              (dat.B365W >= thr) & (dat.B365W <= limit)]
    
    # amount of failed bets            
    lost = dat[(dat.elo_diff > elo) & (dat.rank_diff < -rk) & \
               (dat.B365L >= thr) & (dat.B365L <= limit)]
    
    # How much got back
    cashback = won.B365W.sum()
    
    # invested
    invest = won.shape[0] + lost.shape[0]
    
    # ROI absolute
    gain = cashback - invest
    
    # ROI percentage
    ROI_perc = round((cashback/invest)*100,2)
    
    # ROI performance
    ROI_perf = round((gain/invest)*100,2)
    
    results = [invest, ROI_perf, gain, ]
    
    if verbose:
        print(f'Investment:         {invest}     (Number of matches)')
        print(f'Amount of return:   {round(cashback,2)}')
        print(f'Gain:               {round(gain,2)}')
        print(f'Percentage of ROI:  {ROI_perc} %')
        print(f'Performance of ROI: {ROI_perf} %')
    
    if data_back:
        won['gain'] = won.B365W - 1
        lost['gain'] = -1
        result_df = pd.concat([won, lost])
        result_df.sort_values(by=['Date'], inplace=True, ascending=True)
        result_df['rolling_gain'] = result_df.gain.cumsum()
        
        if rst_idx:
            #result_df.reset_index(drop=True)
            result_df.reset_index(inplace=True)
    
        return result_df
    else:
        return results