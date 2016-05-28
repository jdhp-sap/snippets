#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract simulated camera images from a simtel file.

Inspired by ctapipe/examples/read_hessio_single_tel.py
"""

import argparse
import sys

import ctapipe
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt


# histogram types : [‘bar’ | ‘barstacked’ | ‘step’ | ‘stepfilled’]
HISTOGRAM_TYPE = 'bar'

def show_photoelectron_image_histogram(simtel_file_path, output_file_path, tel_num, event_id, channel=0, quiet=False):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_num])

    event = None

    for ev in source:
        if int(ev.dl0.event_id) == event_id:
            event = ev
            break

    if event is None:
        print("Error: event '{}' not found for telescope '{}'.".format(event_id, tel_num))
        sys.exit(1)

    # GET TIME-VARYING EVENT ##################################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    image_array = data[:, ii]

    # GET INTEGRATED EVENT ####################################################

    # The photoelectron image "event.mc.tel[tel_num].photo_electrons" is a 1D numpy array with the same shape (dtype=int32)
    image_array = event.mc.tel[tel_num].photo_electrons

    # INIT PLOT ###############################################################

    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)

    values, bins, patches = ax.hist(image_array.ravel(),
                                    histtype=HISTOGRAM_TYPE,
                                    #bins=image_array.max() - image_array.min(),
                                    bins=100,
                                    fc='gray',
                                    ec='k')

    ax.set_xlim([image_array.min(), image_array.max()])

    # PLOT ####################################################################

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

    parser.add_argument("--event", "-e", type=int, required=True,
                        metavar="INTEGER",
                        help="The event to extract (event ID)")

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
    event_id = args.event
    quiet = args.quiet
    simtel_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "TEL{:03d}_EV{:05d}_CH{:03d}_PE_HIST.pdf".format(tel_num, event_id, channel)
    else:
        output_file_path = args.output

    # DISPLAY IMAGES ##########################################################

    show_photoelectron_image_histogram(simtel_file_path, output_file_path, tel_num, event_id, channel, quiet)

