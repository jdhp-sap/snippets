#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export the content of a simtel event to a JSON file.
"""

import argparse
import astropy
import json
import numpy as np
import sys

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def recursive_serialize(var):
    node_dict = {}

    try:
        # Node with children
        for k, v in var.items():
            node_dict[str(k)] = recursive_serialize(v)
    except AttributeError:
        # Leaf

        if isinstance(var, astropy.units.quantity.Quantity):
            # astropy.units.quantity.Quantity are not serializables, they should be converted to lists
            return str(var.value) # TODO
        elif isinstance(var, astropy.coordinates.angles.Angle):
            return str(var) # TODO
        elif isinstance(var, astropy.time.core.Time):
            return str(var) # TODO
        elif isinstance(var, set):
            return list(var) # TODO
        elif isinstance(var, np.int32):
            return str(var) # TODO
        elif isinstance(var, np.ndarray):
            # Numpy arrays are not serializables, they should be converted to lists
            return var.tolist()
        else:
            return var

    return node_dict


def get_event_data(simtel_file_path, tel_num, event_id):

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

    event_dict = recursive_serialize(event)
    event_dict["meta"] = recursive_serialize(event.meta)

    return event_dict


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

    # EXPORT THE EVENT TO A JSON FILE #########################################

    data = get_event_data(simtel_file_path, tel_num, event_id)

    file_name = "CT{:03d}_EV{:05d}_FULL_EVENT.json".format(tel_num, event_id)

    with open(file_name, "w") as fd:
        #json.dump(data, fd)                           # no pretty print
        json.dump(data, fd, sort_keys=True, indent=4)  # pretty print format

