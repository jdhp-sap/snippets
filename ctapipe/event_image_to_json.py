#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extract simulated camera images from a simtel file.

Inspired by ctapipe/examples/read_hessio_single_tel.py
"""

import argparse
import sys
import json

import ctapipe
import ctapipe.visualization
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt


def get_image_array(simtel_file_path, tel_num, event_id, channel=0):

    # GET EVENT ###############################################################

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

    # INIT PLOT ###############################################################

    # GET TIME-VARYING EVENT ##################################################

    #data = event.dl0.tel[tel_num].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    image = data[:, ii]

    # GET INTEGRATED EVENT ####################################################

    # The image "event.dl0.tel[tel_num].adc_sums[channel]" is a 1D numpy array (dtype=int32)
    image = event.dl0.tel[tel_num].adc_sums[channel]

    return image


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Display simulated camera images from a simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("--channel", "-c", type=int, default=0,
                        metavar="INTEGER",
                        help="The channel number to query")

    parser.add_argument("--event", "-e", type=int,
                        metavar="INTEGER",
                        help="The event to extract (event ID)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    channel = args.channel
    event_id = args.event
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    image_array = get_image_array(simtel_file_path, tel_num, event_id, channel)
    image = image_array.tolist()

    file_name = "CT{:03d}_EV{:05d}_CH{:03d}.json".format(tel_num, event_id, channel)

    with open(file_name, "w") as fd:
        json.dump(image, fd)                           # no pretty print
        #json.dump(image, fd, sort_keys=True, indent=4)  # pretty print format

