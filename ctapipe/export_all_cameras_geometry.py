#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export to a JSON file the camera's geometry defined in a given simtel file.
"""

import argparse

import ctapipe
from ctapipe.io.hessio import hessio_event_source

import numpy as np
from matplotlib import pyplot as plt

import json

def export_cameras_geometry(simtel_file_path):

    source = hessio_event_source(simtel_file_path)

    tel_id_set = set()

    for event in source:
        for tel_id in event.dl0.tels_with_data:
            tel_id_set.add(tel_id)

    camera_geometry_dict = {}

    for tel_id in tel_id_set:
        x, y = event.meta.pixel_pos[tel_id]
        foclen = event.meta.optical_foclen[tel_id]

        geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

        foclen = float(foclen.value)
        x = np.array([float(v.value) for v in x])
        y = np.array([float(v.value) for v in y])
        cam_id = geom.cam_id
        pix_type = geom.pix_type

        try:
            if cam_id in camera_geometry_dict:
                if camera_geometry_dict[cam_id]["pixel_type"] != pix_type:
                    raise ValueError("{} (pixel_type)".format(cam_id))
                if not np.array_equal(camera_geometry_dict[cam_id]["pixel_pos_x"], x):
                    raise ValueError("{} (pixel_pos_x)".format(cam_id))
                if not np.array_equal(camera_geometry_dict[cam_id]["pixel_pos_y"], y):
                    raise ValueError("{} (pixel_pos_y)".format(cam_id))
                if camera_geometry_dict[cam_id]["foclen"] != foclen:
                    raise ValueError("{} (foclen)".format(cam_id))
                camera_geometry_dict[cam_id]["tel_id_list"].append(tel_id)
            else:
                current_camera_dict = {
                        "pixel_type": pix_type,
                        "pixel_pos_x": x,
                        "pixel_pos_y": y,
                        "foclen": foclen,
                        "tel_id_list": [tel_id]
                        }
                camera_geometry_dict[cam_id] = current_camera_dict
        except ValueError:
            pass # TODO

    # PRINT CAMERAS GEOMETRY ##############################

    for camera_id, camera_dict in camera_geometry_dict.items():
        print(camera_id)
        for k, v in camera_dict.items():
            print(" -", k, v)

    # EXPORT CAMERAS GEOMETRY #############################

    with open("cameras_geometry.json", "w") as fd:
        #json.dump(camera_geometry_dict, fd)                           # no pretty print
        json.dump(camera_geometry_dict, fd, sort_keys=True, indent=4)  # pretty print format


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    desc = "Export to a JSON file the camera's geometry defined in a given simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    simtel_file_path = args.fileargs[0]

    # DISPLAY IMAGES ##########################################################

    export_cameras_geometry(simtel_file_path)

