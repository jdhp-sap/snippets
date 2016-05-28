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

    event_set_list = []

    # For each simtel file...
    for simtel_file_path in simtel_file_path_list:

        event_set = set()   # Set of events (or more exactly pairs (event_id, telescope_id))

        source = hessio_event_source(simtel_file_path, allowed_tels=None, max_events=None)

        for event in source:
            event_id = event.dl0.event_id
            for telescope_id in event.trig.tels_with_trigger:
                event_set.add((int(event_id), int(telescope_id)))

        if len(event_set) > 0:
            event_set_list.append(event_set)

    return event_set_list


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("--operation", "-o",
                        metavar="STRING",
                        help="The operation to apply (union, intersection or difference)")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    operation_str = args.operation
    simtel_file_path_list = args.fileargs

    if operation_str not in ("union", "intersection", "difference"):
        raise(ValueError("Wrong operation identifier"))

    # DISPLAY IMAGES ##########################################################

    event_set_list = event_set_operations(simtel_file_path_list)

    if operation_str == "union":
        event_set = set.union(*event_set_list)
    elif operation_str == "intersection":
        event_set = set.intersection(*event_set_list)
    elif operation_str == "difference":
        set1 = set.union(*event_set_list)
        set2 = set.intersection(*event_set_list)
        event_set = set.difference(set1, set2)
    else:
        raise(ValueError("Wrong operation identifier"))

    for event_id, telescope_id in event_set:
        print(event_id, telescope_id)

