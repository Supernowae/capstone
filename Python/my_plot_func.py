# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:43:33 2020

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt


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


