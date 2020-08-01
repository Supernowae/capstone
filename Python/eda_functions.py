# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:43:33 2020

@author: Supernowae
"""
import numpy as np
import matplotlib.pyplot as plt

########################################
# some plotting functions

def plot_rates_with_tax(rates_nom, rates_eff, rate_eff_1):
    '''
    Plots two subplots. The effective rates vs. nominal rates in two different zoom aspects.
    rates_nom: 1D array of nominal rates. Just a linspace e.g.
    rates_eff: 1D array of tax influenced rates.
    rate_eff_1: int, nominal rate where the efficient rate crosses 1
    '''
    fig, (ax1, ax2) = plt.subplots(1,2,figsize = (15,6))
    fig.suptitle('Effective rates due to tax', fontsize = 16)
    ax1.plot(rates_nom, rates_nom, label = 'rates without tax (nominal)')
    ax1.plot(rates_nom, rates_eff, label = 'rates with tax (effective)')
    
    ax1.legend()
    ax1.set_xlabel('$Rate_{nominal}$', fontsize = 14)
    ax1.set_ylabel('$Rate_{effective}$', fontsize = 14)
    ax1.grid()
    ax1.set_xlim([1, 1.8]);
    ax1.set_ylim([0.92, 1.9]);
    
    ax2.plot([0,5],[1,1],'k-')
    ax2.plot([rate_eff_1,rate_eff_1],[0,5],'k--')
    
    ax2.plot(rates_nom, rates_nom, label = 'rates without tax')
    ax2.plot(rates_nom, rates_eff, label = 'rates with tax')
    
    ax2.legend()
    ax2.grid()
    ax2.set_xlabel('$Rate_{nominal}$', fontsize = 14)
    ax2.set_ylabel('$Rate_{effective}$', fontsize = 14)
    ax2.set_xlim([1, 1.1]);
    ax2.set_ylim([0.92, 1.1]);
    plt.show()
    
    
    


def plot_min_perc_winning(rates_nom, min_win_0,min_win_0_eff):
    '''
    Plots the percentage of won bets that is required to not lose money taking the rate as avarage rate.
    rates_nom: 1D array of nominal rates. Just a linspace e.g.
    min_win_0: 1D array, normally >>> (1/rates_nom)*100
    min_win_0_eff: 1D array, normally >>> (1/rates_eff)*100
    '''
    fig = plt.figure(figsize = (10,5))
    plt.suptitle('Percentage of won bets for not losing money in average', fontsize = 16)
    plt.plot(rates_nom, min_win_0, label = 'without tax')
    plt.plot(rates_nom, min_win_0_eff, label = 'with tax')
    plt.plot(rates_nom[np.where(min_win_0_eff>100)], min_win_0_eff[np.where(min_win_0_eff>100)], 'r--', label = 'not possible')
    plt.grid()
    plt.legend()
    ax = plt.gca()
    
    ax.set_xlabel('$Rate_{nominal}$', fontsize = 14);
    ax.set_ylabel('required percentage of winning [%]', fontsize = 14);
    plt.show()


def plot_delta_hisograms(k1,k2, limit_y, title):
    '''
    k1: 
    k2: 
    limit_y: upper limit of the upper graphs
    title:   title over all
    '''

    f, axs = plt.subplots(2,2,figsize=(15,15))
    f.suptitle(title, fontsize = 16)

    # the histogram of the data
    x = k1.elo_diff
    x2 = k2.elo_diff*(-1)
    n, bins, patches = axs[0][0].hist(x, 50, facecolor='g',range= [0,800], alpha=0.75, label = 'won');
    n2, bins2, patches2 =axs[0][0].hist(x2, bins, facecolor='r', alpha=0.75, label = 'lost');
    axs[0][0].legend();
    axs[0][0].set_xlabel('$\Delta$ elo-score')
    axs[0][0].set_ylabel('amount of matches')
    axs[0][0].set_ylim([0,limit_y]);

    x3 = n/(n+n2)
    width = 0.99* (bins[1] - bins[0])
    axs[1][0].bar(bins[:-1]+width/2, x3,facecolor='g',  width=width);
    #axs[1][0].bar(x3, bins, facecolor='g', alpha=0.75, label = 'won');
    axs[1][0].set_xlabel('$\Delta$ elo-score')
    axs[1][0].set_ylabel('ratio of won matches')
    axs[1][0].set_ylim([0,1.05]);

    x = k1.rank_diff
    x2 = k2.rank_diff*(-1)
    n, bins, patches = axs[0][1].hist(x, 50, facecolor='g', range= [0,400], alpha=0.75, label = 'won');
    n2, bins2, patches2 =axs[0][1].hist(x2, bins, facecolor='r', alpha=0.75, label = 'lost');
    axs[0][1].legend();
    axs[0][1].set_xlabel('$\Delta$ ATP-rank')
    axs[0][1].set_ylabel('amount of matches')
    axs[0][1].set_ylim([0,limit_y]);

    x3 = n/(n+n2)
    width = 0.99* (bins[1] - bins[0])
    axs[1][1].bar(bins[:-1]+width/2, x3,facecolor='g',  width=width);
    axs[1][1].set_xlabel('$\Delta$ ATP-rank')
    axs[1][1].set_ylabel('ratio of won matches')
    axs[1][1].set_ylim([0,1.05]);

##############################################################
# calculating functions


def gain_perc_b365(dat, tax=0.05, round_ = None, limit = 200, threshold = None, diff_elo = 0, diff_rank = 0):
    '''
    OBSOLETE and BUGGY!!!!
    
    Gives back the avarage performace of betting. Staight betting on the player with the better elo-score AND the better Rank.
    
    dat: the given DataFrame.
    tax: tax rate to be considered directly on the wager.
    round_: index of list. selecting the round to be inspected. If None then all rounds are considered.
    ['1st Round', '2nd Round','3rd Round', '4th Round', 'Quarterfinals', 'Semifinals', 'The Final']
    limit: maximum odds to be considered
    thr: minimum odd as theshold for betting. If 'None' then threshold calculated by tax if set.
    diff_elo: how much higher should the elo-score be least.
    diff_rank: how much higher should the rank be least.
    
    return:
    gain: average performance

    (n_bets: number of bets)
    (n_good_bets: number of sucessful bets)
    '''
    
    
    
    #if therhold == None:
    #    thr = 1/(1-tax)
    #else:
    #    thr = threshold
    thr = 1/(1-tax) if threshold == None else threshold
    
    rounds = pd.Series(['1st Round', '2nd Round','3rd Round', '4th Round', 'Quarterfinals', 'Semifinals', 'The Final'])
    
    round_x = None if round_ == None else list([round_]) if type(round_) == int else round_
    rnd = list(rounds) if round_x == None else list(rounds[round_x])
    
    # amount of successfull bets
    #k1 = len(dat.B365W[(dat.elo_winner>dat.elo_loser+diff_elo) & (dat.WRank<dat.LRank-diff_rank) & (dat.B365W>thr) & (dat.B365W<limit) & (dat.Round.isin(rnd))])
    k1 = len(dat.B365W[(dat.elo_winner>dat.elo_loser+diff_elo)  & (dat.B365W>thr) & (dat.B365W<limit) & (dat.Round.isin(rnd))])
    # amount of failed bets    
    #k2 = len(dat.B365W[(dat.elo_winner<dat.elo_loser-diff) & (dat.WRank>dat.LRank+diff_rank) & (dat.B365L>thr) & (dat.B365L<limit) & (dat.Round.isin(rnd))])
    k2 = len(dat.B365W[(dat.elo_winner<dat.elo_loser-diff)  & (dat.B365L>thr) & (dat.B365L<limit) & (dat.Round.isin(rnd))])
    # earnings absolute
    #g = (dat.B365W[(dat.elo_winner>dat.elo_loser+diff_elo)& (dat.WRank<dat.LRank-diff_rank) & (dat.B365W>thr) & (dat.B365W<limit)& (dat.Round.isin(rnd))]*(1-tax)).sum()
    g = (dat.B365W[(dat.elo_winner>dat.elo_loser+diff_elo) & (dat.B365W>thr) & (dat.B365W<limit)& (dat.Round.isin(rnd))]*(1-tax)).sum()
    # earnings percentage of all bets
    #k = ((dat.B365W[(dat.elo_winner>dat.elo_loser+diff_elo)& (dat.WRank<dat.LRank-diff_rank) & (dat.B365W>thr) & (dat.Round.isin(rnd))]*(1-tax)).sum()-(k1+k2))/(k1+k2)
    k = ((dat.B365W[(dat.elo_winner>dat.elo_loser+diff_elo) & (dat.B365W>thr) & (dat.Round.isin(rnd))]*(1-tax)).sum()-(k1+k2))/(k1+k2)
    
    return k, k1, (k1 + k2), g
    #return k
