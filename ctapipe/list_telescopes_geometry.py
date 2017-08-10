#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Print the list of triggered telescopes ID and geometry of the given simtel
file.

Example of output:

    Telescope 001: LSTCam (hexagonal pixels)
    Telescope 002: LSTCam (hexagonal pixels)
    Telescope 003: LSTCam (hexagonal pixels)
    Telescope 004: LSTCam (hexagonal pixels)
    Telescope 005: NectarCam (hexagonal pixels)
    Telescope 006: NectarCam (hexagonal pixels)
    ...
    Telescope 017: FlashCam (hexagonal pixels)
    Telescope 018: FlashCam (hexagonal pixels)
    ...
    Telescope 029: ASTRI (rectangular pixels)
    ...
    Telescope 053: GATE (rectangular pixels)
    ...

"""

import argparse
import json

import ctapipe
from ctapipe.io.hessio import hessio_event_source

from ctapipe.instrument import camera


def list_telescopes_geometry(simtel_file_path):
    """Print the list of triggered telescopes ID and geometry of the
    'simtel_file_path' file.

    Parameters
    ----------
    simtel_file_path : str
        The path of the simtel file to process.
    """

    source = hessio_event_source(simtel_file_path)

    tel_id_set = set()

    for event in source:
        for tel_id in event.dl0.tels_with_data:
            tel_id_set.add(int(tel_id))

    tel_geometry_dict = {}

    for tel_id in tel_id_set:
        x, y = event.inst.pixel_pos[tel_id]
        foclen = event.inst.optical_foclen[tel_id]
        geom = camera.CameraGeometry.guess(x, y, foclen)
        tel_geometry_dict[tel_id] = [geom.cam_id, geom.pix_type]
        print("Telescope {:03d}: {} ({} pixels)".format(tel_id, geom.cam_id, geom.pix_type))

    return tel_geometry_dict


def main():
    """Parse command options (sys.argv)."""

    # PARSE OPTIONS ###########################################################

    desc = "Print the list of triggered telescopes ID and geometry of the given simtel file."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("fileargs", nargs=1, metavar="FILE",
                        help="The simtel file to process")

    args = parser.parse_args()

    simtel_file_path = args.fileargs[0]

    # PRINT THE LIST ##########################################################

    tel_geometry_dict = list_telescopes_geometry(simtel_file_path)

    #for tel_id, (cam_id, pix_type) in tel_geometry_dict.items():
    #    print("Telescope {:03d}: {} ({} pixels)".format(tel_id, cam_id, pix_type))

    # EXPORT CAMERAS GEOMETRY #############################

    output_file_path = simtel_file_path + ".cameras_geometry.json"

    with open(output_file_path, "w") as fd:
        #json.dump(camera_dict, fd)                                 # no pretty print
        json.dump(tel_geometry_dict, fd, sort_keys=True, indent=4)  # pretty print format

if __name__ == '__main__':
    main()
