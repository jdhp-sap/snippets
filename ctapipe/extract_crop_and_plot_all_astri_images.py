#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Jérémie DECOCK (http://www.jdhp.org)

# This script is provided under the terms and conditions of the MIT license:
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
... TODO
"""

__all__ = ['extract_images',
           'crop_astri_image']

import argparse
from astropy.io import fits
import numpy as np
import os
import sys

import ctapipe
from ctapipe.io.hessio import hessio_event_source
import pyhessio

DEFAULT_TEL_FILTER = list(range(1, 34))   # TODO

def get_mc_calibration_coeffs(tel_id):
    """
    Get the calibration coefficients from the MC data file to the data.
    This is ahack (until we have a real data structure for the calibrated
    data), it should move into `ctapipe.io.hessio_event_source`.

    Parameters
    ----------
    tel_id : int
        The ID of the telescope to process.

    Returns
    -------
    tuple of Numpy array
        A tuble containing 2 elements: ``pedestal`` a 2D arrays of the pedestal
        (one dimension for each channel) and ``gain`` a 2D arrays of the PE/DC
        ratios (one dimension for each channel).
    """
    pedestal = pyhessio.get_pedestal(tel_id)
    gains = pyhessio.get_calibration(tel_id)

    return pedestal, gains


def apply_mc_calibration(adcs, tel_id, adc_treshold=3500.):
    """
    Apply basic calibration.

    Parameters
    ----------
    adc : Numpy array
        The uncalibrated ADC signal (one dimension per channel).
    tel_id : int
        The ID of the telescope to process.

    Returns
    -------
    Numpy array
        A tuble containing 2 elements: ``pedestal`` a 2D arrays of the pedestal
        (one dimension for each channel) and ``gain`` a 2D arrays of the PE/DC
        ratios (one dimension for each channel).
    """

    peds, gains = get_mc_calibration_coeffs(tel_id)

    peds_ch0 = peds[0]
    peds_ch1 = peds[1]

    # TODO ???
    #calibrated_image = ((adc - peds[:, np.newaxis] / adc.shape[1]) * gains[:, np.newaxis])
    # calibrated_image = (adc - peds) * gains

    calibrated_image = [ (adc0 - ped0) * gain0 if adc0 < adc_treshold else (adc1 - ped1) * gain1
                         for adc0, adc1, ped0, ped1, gain0, gain1
                         in zip(adcs[0], adcs[1], peds[0], peds[1], gains[0], gains[1]) ]

    return np.array(calibrated_image)


def extract_images(simtel_file_path,
                   tel_id_filter_list=None,
                   event_id_filter_list=None,
                   output_directory=None):

    # EXTRACT IMAGES ##########################################################

    # hessio_event_source returns a Python generator that streams data from an
    # EventIO/HESSIO MC data file (e.g. a standard CTA data file).
    # This generator contains ctapipe.core.Container instances ("event").
    #
    # Parameters:
    # - max_events: maximum number of events to read
    # - allowed_tels: select only a subset of telescope, if None, all are read.
    source = hessio_event_source(simtel_file_path, allowed_tels=tel_id_filter_list)

    # ITERATE OVER EVENTS #####################################################

    for event in source:

        event_id = int(event.dl0.event_id)

        if (event_id_filter_list is None) or (event_id in event_id_filter_list):

            print("event", event_id)

            # ITERATE OVER IMAGES #############################################

            for tel_id in event.trig.tels_with_trigger:

                tel_id = int(tel_id)

                if tel_id in tel_id_filter_list:

                    print("telescope", tel_id)

                    # CHECK THE IMAGE GEOMETRY (ASTRI ONLY) ###################

                    # TODO

                    print("checking geometry")

                    x, y = event.meta.pixel_pos[tel_id]
                    foclen = event.meta.optical_foclen[tel_id]
                    geom = ctapipe.io.CameraGeometry.guess(x, y, foclen)

                    if (geom.pix_type != "rectangular") or (geom.cam_id != "ASTRI"):
                        raise ValueError("Telescope {}: error (the input image is not a valide ASTRI telescope image)".format(tel_id))

                    # GET AND CROP THE IMAGE ##################################

                    # uncalibrated_image = [1D numpy array of channel1, 1D numpy array of channel2]
                    # calibrated_image = 1D numpy array

                    print("calibrating")

                    adc_channel_0 = event.dl0.tel[tel_id].adc_sums[0]      # TODO
                    adc_channel_1 = event.dl0.tel[tel_id].adc_sums[1]      # TODO
                    uncalibrated_image = np.array([adc_channel_0, adc_channel_1])

                    calibrated_image = apply_mc_calibration(uncalibrated_image, tel_id)

                    print("cropping ADC image")

                    cropped_img = crop_astri_image(calibrated_image)

                    # GET AND CROP THE PHOTOELECTRON IMAGE ####################

                    pe_image = event.mc.tel[tel_id].photo_electrons   # 1D np array

                    print("cropping PE image")

                    cropped_pe_img = crop_astri_image(pe_image)

                    # SAVE THE IMAGE ##########################################

                    output_file_path_template = "{}_EV{:05d}_TEL{:03d}.fits"

                    if output_directory is not None:
                        simtel_basename = os.path.basename(simtel_file_path)
                        prefix = os.path.join(output_directory, simtel_basename)
                    else:
                        prefix = simtel_file_path

                    output_file_path = output_file_path_template.format(prefix,
                                                                        event_id,
                                                                        tel_id)

                    print("saving", output_file_path)

                    metadata = {}
                    metadata['tel_id']=tel_id
                    metadata['opt_focl']=quantity_to_tuple(event.meta.optical_foclen[tel_id],'m')

                    metadata['event_id']=event_id
                    metadata['mc_energ']= quantity_to_tuple(event.mc.energy,'TeV')

                    metadata['mc_az']= quantity_to_tuple(event.mc.az,'rad')
                    metadata['mc_alt']= quantity_to_tuple(event.mc.alt,'rad')

                    metadata['mc_corex']= quantity_to_tuple(event.mc.core_x,'m')
                    metadata['mc_corey']=quantity_to_tuple(event.mc.core_y,'m')

                    save_fits(cropped_img, cropped_pe_img, output_file_path, metadata)


def crop_astri_image(input_img):
    """
    Crop images comming form "ASTRI" telescopes in order to get regular 2D "rectangular"
    images directly usable with most image processing tools.

    Parameters
    ----------
    input_img : numpy.array
        The image to crop

    Returns
    -------
    A numpy.array containing the cropped image.
    """

    # Check the image
    if len(input_img) != (37*64):
        raise ValueError("The input image is not a valide ASTRI telescope image.")

    # Make the transformation map
    img_map = np.zeros([8*5, 8*5], dtype=int)

    img_map[0*8:1*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 29 * 64
    img_map[0*8:1*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 30 * 64
    img_map[0*8:1*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 31 * 64
    img_map[0*8:1*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 32 * 64
    img_map[0*8:1*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 33 * 64

    img_map[1*8:2*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 23 * 64
    img_map[1*8:2*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 24 * 64
    img_map[1*8:2*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 25 * 64
    img_map[1*8:2*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 26 * 64
    img_map[1*8:2*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 27 * 64

    img_map[2*8:3*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] + 16 * 64
    img_map[2*8:3*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 17 * 64
    img_map[2*8:3*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 18 * 64
    img_map[2*8:3*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 19 * 64
    img_map[2*8:3*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 20 * 64

    img_map[3*8:4*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  9 * 64
    img_map[3*8:4*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] + 10 * 64
    img_map[3*8:4*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] + 11 * 64
    img_map[3*8:4*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] + 12 * 64
    img_map[3*8:4*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] + 13 * 64

    img_map[4*8:5*8, 0*8:1*8] = np.arange(64).reshape([8,8])[::-1,:] +  3 * 64
    img_map[4*8:5*8, 1*8:2*8] = np.arange(64).reshape([8,8])[::-1,:] +  4 * 64
    img_map[4*8:5*8, 2*8:3*8] = np.arange(64).reshape([8,8])[::-1,:] +  5 * 64
    img_map[4*8:5*8, 3*8:4*8] = np.arange(64).reshape([8,8])[::-1,:] +  6 * 64
    img_map[4*8:5*8, 4*8:5*8] = np.arange(64).reshape([8,8])[::-1,:] +  7 * 64

    # Make the output image
    cropped_img = input_img[[img_map.ravel()]].reshape([8*5, 8*5])

    return cropped_img


def save_fits(img, pe_img, output_file_path, metadata):
    """
    img is the image and it should be a 2D or a 3D numpy array with values.
    """

    if img.ndim not in (2, 3):
        raise Exception("The input image should be a 2D or a 3D numpy array.")

    # http://docs.astropy.org/en/stable/io/fits/appendix/faq.html#how-do-i-create-a-multi-extension-fits-file-from-scratch
    hdu0 = fits.PrimaryHDU(img)
    hdu1 = fits.ImageHDU(pe_img)

    hdu_list = fits.HDUList([hdu0, hdu1])

    for key, val in metadata.items():
        if type(val) is tuple :
            hdu_list[0].header[key] = val[0]
            hdu_list[0].header.comments[key] = val[1]
        else:
            hdu_list[0].header[key] = val

    if os.path.isfile(output_file_path):
        os.remove(output_file_path)

    hdu_list.writeto(output_file_path)

           
def quantity_to_tuple(qt, unit_str):
    """
    Splits a quantity into a tuple of (value,unit) where unit is FITS complient.
    Useful to write FITS header keywords with units in a comment.
    Parameters
    ----------
    qt : astropy quantity

    unit_str: str
        unit string representation readable by astropy.units (e.g. 'm', 'TeV', etc)

    """
    return qt.to(unit_str).value, qt.to(unit_str).unit.to_string(format='FITS')


def main():

    # PARSE OPTIONS ###########################################################

    desc = "TODO."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--telescope", "-t",
                        metavar="INTEGER LIST",
                        help="The telescopes to query (telescopes number separated by a comma)")

    parser.add_argument("--event", "-e",
                        metavar="INTEGER LIST",
                        help="The events to extract (events ID separated by a comma)")

    parser.add_argument("--output", "-o",
                        metavar="DIRECTORY",
                        help="The output directory")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The simtel files to process")

    args = parser.parse_args()

    if args.telescope is None:
        tel_id_filter_list = DEFAULT_TEL_FILTER
    else:
        tel_id_filter_list = [int(tel_id_str) for tel_id_str in args.telescope.split(",")]

    if args.event is None:
        event_id_filter_list = None
    else:
        event_id_filter_list = [int(event_id_str) for event_id_str in args.event.split(",")]

    print("Telescopes:", tel_id_filter_list)
    print("Events:", event_id_filter_list)

    output_directory = args.output
    simtel_file_path_list = args.fileargs

    if output_directory is not None:
        if not (os.path.exists(output_directory) and os.path.isdir(output_directory)):
            raise Exception("{} does not exist or is not a directory.".format(output_directory))

    # ITERATE OVER SIMTEL FILES ###############################################

    for simtel_file_path in simtel_file_path_list:

        print("Processing", simtel_file_path)

        # EXTRACT, CROP AND SAVE THE IMAGES ###################################

        extract_images(simtel_file_path, tel_id_filter_list, event_id_filter_list, output_directory)


if __name__ == "__main__":
    main()
