#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export to a JSON file the camera's geometry defined in a given simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt

import json

def export_cameras_geometry(simtel_file_path, tel_id):

    source = hessio_event_source(simtel_file_path)

    for event in source:
        #######################################################################
        # CAUTION:                                                            #
        # event.meta.optical_foclen and event.meta.tel_pos are only filled    #
        # when source is traversed !                                          #
        # The current value of these two variables is not the actual value    #
        # for the current event but the cumulated value of past events !      #
        #######################################################################

        print("Event", event.dl0.event_id)
        #print("tels_with_trigger", event.trig.tels_with_trigger)
        #print("tels_with_data", event.dl0.tels_with_data)
        #print("optical_foclen", event.meta.optical_foclen)
        #print("tel_pos", event.meta.tel_pos)

    # GET CAMERAS GEOMETRY ################################
    
    x, y = event.meta.pixel_pos[tel_id]
    foclen = event.meta.optical_foclen[tel_id]

    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

    foclen = float(foclen.value)
    x = [float(v.value) for v in x]
    y = [float(v.value) for v in y]
    cam_id = geom.cam_id
    pix_type = geom.pix_type

    camera_dict = {
            "camera_id": cam_id,
            "pixel_type": pix_type,
            "pixel_pos_x": x,
            "pixel_pos_y": y,
            "foclen": foclen,
            "tel_id": tel_id
            }

    # PRINT CAMERAS GEOMETRY ##############################

    for k, v in camera_dict.items():
        print("- ", k, v)

    # EXPORT CAMERAS GEOMETRY #############################

    with open("cameras_geometry_tel{:03d}.json".format(tel_id), "w") as fd:
        #json.dump(camera_dict, fd)                           # no pretty print
        json.dump(camera_dict, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Export to a JSON file the camera's geometry defined in a given simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t", type=int, required=True,
                        metavar="INTEGER",
                        help="The telescope to query (telescope number)")

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    tel_id = args.telescope
    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    export_cameras_geometry(simtel_file_path, tel_id)

