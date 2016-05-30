#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Do set operations on event sets.

This script has been made to be used by shell scripts.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def event_set_operations(simtel_file_path_list):

    event_set_dict = {}

    # For each simtel file...
    for simtel_file_path in simtel_file_path_list:

        event_set = set()   # Set of events (or more exactly pairs (event_id, telescope_id))

        source = hessio_event_source(simtel_file_path, allowed_tels=None, max_events=None)

        for event in source:
            event_id = event.dl0.event_id
            for telescope_id in event.trig.tels_with_trigger:
                event_set.add((int(event_id), int(telescope_id)))

        if len(event_set) > 0:
            # Ignore empty simtel files
            event_set_dict[simtel_file_path] = event_set

    return event_set_dict


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List (event, telescope) pairs commons to given simtel files.")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The simtel files to process")

    args = parser.parse_args()
    simtel_file_path_list = args.fileargs

    # MAKE COMMON EVENTS SET ##################################################

    event_set_dict = event_set_operations(simtel_file_path_list)

    event_set = set.intersection(*event_set_dict.values())

    for simtel_file_path in event_set_dict.keys():
        for event_id, telescope_id in event_set:
            print(simtel_file_path, event_id, telescope_id)

