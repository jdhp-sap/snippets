#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
List events of a simtel file.

This script has been made to be used by shell scripts.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def list_simtel_events(simtel_file_path):

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

    event_list = []   # List of events per telescope

    for event in source:
        event_id = event.dl0.event_id
        for telescope_id in event.trig.tels_with_trigger:
            event_list.append((int(event_id), int(telescope_id)))

    return event_list


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    event_list = list_simtel_events(simtel_file_path)

    for event_id, telescopes_id in event_list:
        print("{:06} {:03}".format(event_id, telescopes_id))

