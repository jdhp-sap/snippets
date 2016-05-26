#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
List events for each telescope in a simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source


def list_simtel_events_per_telescope(simtel_file_path):

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

    events_per_tel_dict = {}   # List of events per telescope

    for event in source:
        for telescope_id in event["trig"]["tels_with_trigger"]:
            if telescope_id not in events_per_tel_dict:
                events_per_tel_dict[telescope_id] = []
            events_per_tel_dict[telescope_id].append(event["dl0"]["event_id"])

    return events_per_tel_dict


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="List simtel content.")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    events_per_tel_dict = list_simtel_events_per_telescope(simtel_file_path)

    print("Events per telescope:")
    for telescope_id, events_id_list in events_per_tel_dict.items():
        #num_events = len(events_id_list)
        #print("- Telescope {:03}: {:03} event{} {}".format(telescope_id,
        #                                                   num_events,
        #                                                   "s" if num_events > 1 else " ",
        #                                                   events_id_list))
        print("- Telescope {:03}: {}".format(telescope_id, events_id_list))

