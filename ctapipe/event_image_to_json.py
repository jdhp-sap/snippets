#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export a simtel camera image to a JSON file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt

import json

import sys


def get_image_array(simtel_file_path, tel_id, event_id):

    # GET EVENT ###############################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    # 
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=[tel_id])

    event = None

    for ev in source:
        if int(ev.dl0.event_id) == event_id:
            event = ev
            break

    if event is None:
        print("Error: event '{}' not found for telescope '{}'.".format(event_id, tel_id))
        sys.exit(1)

    # GET IMAGE ###############################################################

    # GET TIME-VARYING EVENT

    #data = event.dl0.tel[tel_id].adc_samples[channel]
    #for ii in range(data.shape[1]):
    #    image = data[:, ii]

    # GET INTEGRATED EVENT

    channel = 0       # TODO: save all channels
    image = event.dl0.tel[tel_id].adc_sums[channel]

    # GET PHOTOELECTRON IMAGE #################################################

    pe_image = event.mc.tel[tel_id].photo_electrons

    # GET CAMERA GEOMETRY #####################################################
    
    x, y = event.meta.pixel_pos[tel_id]
    foclen = event.meta.optical_foclen[tel_id]

    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    # MAKE THE IMAGE DICT #####################################################

    image_dict = {
            "event_id": event_id,
            "tel_id": tel_id,
            "image": image.tolist(),
            "photoelectron_image": pe_image.tolist(),
            "camera_id": geom.cam_id,
            "pixel_type": geom.pix_type,
            "foclen": float(foclen.value),
            "telescope_position": [float(v) for v in event.meta.tel_pos],
            "pixel_pos_x": [float(v.value) for v in x],
            "pixel_pos_y": [float(v.value) for v in y],
            "simtel_file": event.meta.hessio__input
            }

    return image_dict


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Export a simtel camera image to a JSON file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("--event", "-e", type=int, required=True,
                        metavar="INTEGER",
                        help="The event to extract (event ID)")

    parser.add_argument("--output", "-o", default=None,
                        metavar="FILE",
                        help="The output file path")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_id = args.telescope
    event_id = args.event
    simtel_file_path = args.fileargs[0]

    if args.output is None:
        output_file_path = "TEL{:03d}_EV{:05d}.json".format(tel_id, event_id)
    else:
        output_file_path = args.output

    # EXPORT THE IMAGE AND METAS TO A JSON FILE ###############################

    image_dict = get_image_array(simtel_file_path, tel_id, event_id)

    with open(output_file_path, "w") as fd:
        #json.dump(image_dict, fd)                           # no pretty print
        json.dump(image_dict, fd, sort_keys=True, indent=4)  # pretty print format

