import pandas as pd
from random import randrange
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn')
#---------ANALYSIS---------------------
DJI = pd.read_csv('DJI.csv')

mean = DJI['Returns'].mean()
std = DJI['Returns'].std()

#plt.axvline(x = mean, color='r', linestyle='-', alpha=0.7, label = 'mean')
# plt.axvline(x = mean + std, color='r', linestyle='-', alpha=0.7, label = 'mean')
plt.axvline(x = mean + 2*std, color='r', linestyle='-', alpha=0.5, label = 'mean')
# plt.axvline(x = mean + 3*std, color='r', linestyle='-', alpha=0.7, label = 'mean')
# plt.axvline(x = mean - std, color='r', linestyle='-', alpha=0.7, label = 'mean')
plt.axvline(x = mean - 2*std, color='r', linestyle='-', alpha=0.5, label = 'mean')
# plt.axvline(x = mean - 3*std, color='r', linestyle='-', alpha=0.7, label = 'mean')

title = str('95% of returns are in {:.2f}'.format(1+mean-2*std) + ' and {:.2f}'.format(1+mean+2*std))
DJI['Returns'].hist(bins=15)

plt.title(title)
plt.show()


#---------MONTE CARLO-------------------

INITIAL_INVESTMENT = 5000
MONTHLY_TOPUP = 400
YEARLY = MONTHLY_TOPUP * 12
# ------------------------------------
RAND_TOP = 148
RAND_BOT = 68
YEAR = 34

saving = [INITIAL_INVESTMENT]

for i in range(1, 35):
    saving.append((saving[i - 1]) + YEARLY)

capital = pd.DataFrame(saving, columns=['saving'])

for k in range(1, 50):
    capital[str('capital' + str(k))] = capital['saving']
    for i in range(1, len(capital)):
        capital.loc[i, str('capital' + str(k))] = (capital.loc[i - 1, str('capital' + str(k))] + YEARLY) * float(
            randrange(RAND_BOT, RAND_TOP) / 100)

capital['mean'] = capital.median(axis=1)
capital['min'] = capital.min(axis=1)
capital['max'] = capital.max(axis=1)


fig = plt.figure(figsize=(12, 6))
fig.suptitle(('Average return after ' + str(YEAR) + ' years is %.2f' % capital['mean'][capital.index[YEAR]]))
ax = fig.add_subplot(121)
ax2 = fig.add_subplot(122)


capital.plot(legend=None,alpha=0.3, title = 'Monte Carlo Simulations', xlabel = 'Years', ylabel = 'RM', ax = ax)
# capital.plot(y='saving', color = 'red', alpha = 1, ax = ax, label="Savings")
# capital.plot(y='mean', color='green', alpha = 1, ax = ax, label="Average Scenario")

capital.iloc[-1].hist(bins=20, orientation="horizontal", color="pink", alpha=0.5,ax = ax)

capital.plot(y='saving', color = 'red', alpha = 1, label="Savings", xlabel = 'Years', ylabel = 'RM', title = 'Median of simulations', ax = ax2)
capital.plot(y='mean', color='green', alpha = 1, ax = ax2)
# capital.plot(y='min', color='green', alpha = 1, ax = ax2)
# capital.plot(y='max', color='green', alpha = 1, ax = ax2)




# plt.axhline(y=capital['saving'][capital.index[-1]], color='r', linestyle='-', alpha=0.7)
# plt.axhline(y=capital['mean'][capital.index[-1]], color='b', linestyle='-', alpha=0.7)

plt.show()
print(capital)

