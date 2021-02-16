import pandas as pd
from random import randrange
from random import gauss
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')

#---------ANALYSIS---------------------
def cagr(first, last, num_periods):
    
    return ((first / last) ** (1 / (num_periods - 1)) - 1)*100.0

def calculate(initial = 0, monthly = 0, years = 0):
    COMMS = 1.055
    
    data = np.array([0.019,0.073,0.223,-0.056,0.251,0.134,-0.022,0.075,0.265,0.073,0.055,0.11,0.188,-0.338,0.064,0.163,-0.006,0.032,0.253,-0.168,-0.071,-0.062,0.252,0.161,0.226,0.26,0.335,0.021,0.137,0.042,0.203,-0.043,0.27,0.119,0.023,0.226,0.277,-0.037,0.203,0.196,-0.092,0.149,0.042,-0.032,-0.173,0.179,0.383,-0.276,-0.166,0.146,0.061,0.048,-0.152,0.043,0.152,-0.189,0.109,0.146,0.17,-0.108,0.187,-0.093,0.164,0.34,-0.128,0.023,0.208,0.44,-0.038,0.084,0.144,0.176,0.129,-0.021,0.022,-0.081,0.267,0.121,0.138,0.076,-0.154,-0.127,-0.029,0.281,-0.328,0.248,0.385,0.041,0.667,-0.231,-0.527,-0.338,-0.172,0.495,0.277,0.041,0.254,0.262,-0.027,0.215,0.123,-0.329,0.305,0.105,-0.217,-0.042,0.815])
    DJI = pd.DataFrame(data,columns=['Returns'])

    mean = DJI['Returns'].mean()
    std = DJI['Returns'].std()

    from scipy.stats import norm
    import matplotlib.mlab as mlab

    #---------MONTE CARLO-------------------

    if initial == 0:
        INITIAL_INVESTMENT = 2000/COMMS
    else:
        INITIAL_INVESTMENT = float(initial)/COMMS
        
    if monthly == 0:
        MONTHLY_TOPUP = 300/COMMS
    else:
        MONTHLY_TOPUP = float(monthly)/COMMS
        
    if years == 0 :
        YEAR_CHECKPOINT = 10
    else:
        YEAR_CHECKPOINT = int(years)
        
    # ------------------------------------
    YEAR = 30
    SAMPLE = 100
    YEARLY = MONTHLY_TOPUP * 12
    saving = [INITIAL_INVESTMENT]

    for i in range(1, (YEAR+1)):
        saving.append((saving[i - 1]) + YEARLY)

    capital = pd.DataFrame(saving, columns=['saving'])

    for k in range(1, SAMPLE):
        capital[str('capital' + str(k))] = capital['saving']
        for i in range(1, len(capital)):
            ret = gauss(mean,std) + 1

            capital.loc[i, str('capital' + str(k))] = (capital.loc[i - 1, str('capital' + str(k))] + YEARLY) * float(ret)

    total = capital.iloc[YEAR_CHECKPOINT].values.tolist()
    wins = sum(i > capital.iloc[YEAR_CHECKPOINT]['saving'] for i in total)
    winrate = (wins/SAMPLE)*100

    capital['mean'] = capital.median(axis=1)
    capital['min'] = capital.min(axis=1)
    capital['max'] = capital.max(axis=1)
    capital['25th'] = capital.quantile(0.25, axis = 1)
    capital['75th'] = capital.quantile(0.75, axis = 1)
    capital['95th'] = capital.quantile(0.95, axis = 1)

    fig = plt.figure(figsize=(12, 6))
    fig.suptitle(('Average return after ' + str(YEAR_CHECKPOINT) + ' years is between %.2f ' %
                  capital['25th'][capital.index[YEAR_CHECKPOINT]]) + 'and %.2f' % capital['75th'][capital.index[YEAR_CHECKPOINT]]
                 + "\nWin Rate at " + str(YEAR_CHECKPOINT) + " years is " + str(winrate) + "%")
    ax = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax.fill_between(capital.index,capital['25th'], capital['75th'], color='lightgreen',alpha = 0.5)

    capital.plot(y='25th',label="75% of having at least",alpha=0.75, title = 'Monte Carlo Simulations', xlabel = 'Years', ylabel = 'RM', ax = ax)
    capital.plot(y='75th',label="25% of having at least",alpha=0.75, title = 'Monte Carlo Simulations', xlabel = 'Years', ylabel = 'RM', ax = ax)
    capital.plot(y='saving',label="Capital Invested",alpha=0.9, title = 'Monte Carlo Simulations', xlabel = 'Years', ylabel = 'RM', ax = ax)

    ax2.fill_between(capital.index,capital['25th'], capital['75th'], color='lightgreen',alpha = 0.5)

    capital.plot(y='saving', color = 'red', alpha = 1, label="Savings", xlabel = 'Years', ylabel = 'RM', title = 'Median of simulations', ax = ax2)
    capital.plot(y='75th',label="25% of having at least",alpha=0.75, title = 'Monte Carlo Simulations', xlabel = 'Years', ylabel = 'RM', ax = ax2)
    capital.plot(y='25th',label="75% of having at least",alpha=0.75, title = 'Monte Carlo Simulations', xlabel = 'Years', ylabel = 'RM', ax = ax2)
    ax2.set_xlim(0,YEAR_CHECKPOINT)
    ax2.set_ylim(0,capital['95th'][capital.index[YEAR_CHECKPOINT]])

    inv = capital['saving'].iloc[YEAR_CHECKPOINT]
    ret = capital['mean'].iloc[YEAR_CHECKPOINT]
    ret25 = capital['75th'].iloc[YEAR_CHECKPOINT]
    
    print("50% chance of getting return of : {:.2f}".format((ret-inv)/inv))
    print("25% chance of getting return of : {:.2f}".format((ret25-inv)/inv))
    plt.show()