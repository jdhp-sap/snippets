#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Show the content of a simtel event.
"""

import argparse
import numpy as np
import sys

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def recursive_print(var, level=0):
    pre = 3 * level * " "
    try:
        for k, v in var.items():
            print("{}- {}:".format(pre, k))
            recursive_print(v, level+1)
    except AttributeError:
        if isinstance(var, np.ndarray):
            if var.shape == ():
                print("{}- {}   {}, shape={}, dtype={}".format(pre, var, type(var), var.shape, var.dtype))
            else:
                print("{}- [...]   {}, shape={}, dtype={}".format(pre, type(var), var.shape, var.dtype))
        else:
            print("{}- {}   {}".format(pre, var, type(var)))


def list_simtel_content(simtel_file_path, tel_num, event_id):

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

    # DISPLAY EVENT INFORMATIONS ##############################################

    print("- event:")
    recursive_print(event, level=1)
    print("- event.meta:")
    recursive_print(event.meta, level=1)


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Display events info.")

    parser.add_argument("--telescope", "-t", type=int,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("--event", "-e", type=int,
                        metavar="INTEGER",
                        help="The event to extract (event ID)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_num = args.telescope
    event_id = args.event
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    list_simtel_content(simtel_file_path, tel_num, event_id)

