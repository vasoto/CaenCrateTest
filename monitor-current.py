import argparse
import time
from typing import List
import matplotlib.pyplot as plt
import math
from SndCaenManager import SndCaenManager


def main():
    parser = argparse.ArgumentParser(
        'Show a live figure of the currents level of the daq boards')
    #parser.add_argument('mode', type=str, help='Precise the operaton mode (on or off)')
    parser.add_argument('--daqs',
                        nargs='+',
                        default=None,
                        help='Precise the DAQ boards')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    confPath = 'config_SND.toml'
    manager = SndCaenManager(confPath)

    monitor_current(args.daqs, manager, verbose=args.verbose)


def monitor_current(daqs, manager: SndCaenManager, **kwargs):
    nb_daqs = 30
    if daqs is not None:
        nb_daqs = len(daqs)
    x: List = []
    currents: List = [[] for _ in range(nb_daqs)]
    lines = []
    compteur = 0
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylabel('Current [uA]')
    plt.xlabel('Time [cycle]')
    if nb_daqs != 30:
        for i in range(0, nb_daqs):
            line_temp, = ax.plot(x, currents[i])
            lines.append(line_temp)
    if nb_daqs == 30:
        for i in range(0, nb_daqs):
            if math.floor(i / 10) == 0:
                line_temp, = ax.plot(x, currents[i], '-')
            if math.floor(i / 10) == 1:
                line_temp, = ax.plot(x, currents[i], '--')
            if math.floor(i / 10) == 2:
                line_temp, = ax.plot(x, currents[i], '.')
            lines.append(line_temp)

    legend = daqs
    if daqs is None:
        legend = [daq for daq in manager.config['bias'] if daq != 'default']

    ax.legend(lines, legend)

    try:
        while True:
            i = 0
            x.append(compteur)
            compteur += 1
            if daqs is None:
                for daq in manager.config['bias']:
                    if daq != 'default':
                        currents[i].append(
                            manager.getChannelParameter('IMon', 'bias', daq))
                        lines[i].set_data(x, currents[i])
                        i += 1
            else:
                for daq in daqs:
                    currents[i].append(
                        manager.getChannelParameter('IMon', 'bias', daq))
                    lines[i].set_data(x, currents[i])
                    i += 1

            ax.set_xlim([min(x), max(x)])
            min_y = min(map(lambda ls: min(ls), currents))
            max_y = max(map(lambda ls: max(ls), currents))

            ax.set_ylim([min_y - 0.2, max_y + 0.2])
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    """
    current = []
    compteur = 0
    plt.ion()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylabel('Current [uA]')
    plt.xlabel('Time [cylce]')
    line1, = ax.plot(x, current, 'r-')

    while True:
        current.append(manager.getChannelParameter('IMon', 'bias', 'm1x1'))
        x.append(compteur)
        compteur += 1
        ax.set_xlim([min(x), max(x)])
        ax.set_ylim([min(current) - 0.2, max(current) + 0.2])
        line1.set_data(x, current)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1)
    """


if __name__ == '__main__':
    main()
