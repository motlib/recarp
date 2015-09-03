'''
Created on Aug 27, 2015

@author: ultrabene
'''

import matplotlib.pyplot as plt


def plot_binary(data):
    plt.figure()
    plt.subplots_adjust(hspace=0)

    # Get max x
    xmax = max([len(val.off) for val in data.values()])

    nrows = len(data)
    ncols = 1
    ax = None
    for plt_number, key in enumerate(data):
        plt_number += 1

        ax = plt.subplot(nrows, ncols, plt_number, sharex=ax)
        plt.plot(
            data[key].off_binary, label=key, drawstyle='steps-post')
        plt.axis(ymin=-0.1, ymax=1.5, xmin=0, xmax=xmax)
        plt.grid(xdata=range(129))
#         plt.legend()
#         plt.legend(loc=2)
        plt.yticks([0, 1])
