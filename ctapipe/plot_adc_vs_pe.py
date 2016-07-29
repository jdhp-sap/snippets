#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot the ADC signal vs PE for one given telescope (on all events of a given
simtel file).
"""

import argparse

import ctapipe
import ctapipe.visualization
from ctapipe.io.hessio import hessio_event_source

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm


def plot_data(simtel_file_path, output_file_path, tel_num, channel=0, quiet=False):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_num])

    adc_list = []
    pe_list = []

    for event in source:
        # Get ADC image
        adc_list.extend(event.dl0.tel[tel_num].adc_sums[channel].tolist())

        # Get photoelectron image
        pe_list.extend(event.mc.tel[tel_num].photo_electrons.tolist())


    # INIT PLOT ###############################################################

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    ax.plot(pe_list, adc_list, '.')

    #H = ax.hist2d(pe_list, adc_list, bins=1000, norm=LogNorm())
    #fig.colorbar(H[3], ax=ax)

    #ax.set_xlim([0, 60])

    ax.set_title("Telescope {:03d} - Channel {}".format(tel_num, channel))

    ax.set_xlabel("PE", fontsize=24)
    ax.set_ylabel("ADC", fontsize=24)

    # PLOT ####################################################################

    #plt.savefig(output_file_path, bbox_inches='tight')
    plt.savefig(output_file_path)

    if not quiet:
        plt.show()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("--channel", "-c", type=int, default=0,
                        metavar="INTEGER",
                        help="The channel number to query")

    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Don't show the plot, just save it")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    quiet = args.quiet
    simtel_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "TEL{:03d}_CH{}_ADC_vs_PE.png".format(tel_num, channel)
    else:
        output_file_path = args.output

    # DISPLAY IMAGES ##########################################################

    plot_data(simtel_file_path, output_file_path, tel_num, channel, quiet)

