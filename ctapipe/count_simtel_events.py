#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Count the number of events in a simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def count_simtel_events(simtel_file_path):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    #
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path,
                                 allowed_tels=None,
                                 max_events=None)

    num_event_dict = {}   # Number of events per telescope
    total_num_events = 0  # Total number of events

    for event in source:
        total_num_events += 1

        for telescope_id in event["trig"]["tels_with_trigger"]:
            if telescope_id not in num_event_dict:
                num_event_dict[telescope_id] = 0
            num_event_dict[telescope_id] += 1

    return num_event_dict, total_num_events


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    num_event_dict, total_num_events = count_simtel_events(simtel_file_path)

    print("Number of events per telescope:")
    for telescope_id, num_events in num_event_dict.items():
        print("- Telescope {:03}: {} event{}".format(telescope_id, num_events, "s" if num_events > 1 else ""))

    print()
    print("Total number of events:", total_num_events)

