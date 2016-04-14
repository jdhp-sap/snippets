#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
List the content of a simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def list_simtel_content(simtel_file_path):

    # GET EVENT #############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # Source contains few events (usually 0, 1 or 2)
    # 
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path,
                                 allowed_tels=[1],  
                                 max_events=1)

    for event in source:
        print("Count:", event["count"])
        print("Trigger data:", event["trig"])
        print("Monte-Carlo shower data:", event["mc"])
        print("Raw data:", event["dl0"])

        #print("Simtel file path:", event.meta["hessio__input"])
        print("Pixel pos:", event.meta["pixel_pos"])
        #print("Max events:", event.meta["hessio__max_events"])

        print()


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    list_simtel_content(simtel_file_path)

