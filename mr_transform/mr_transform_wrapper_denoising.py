#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: http://docs.astropy.org/en/stable/io/fits/index.html

import argparse
from astropy.io import fits

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

MR_OUTPUT_FILE_PATH = "out.fits"


def get_image_array_from_fits_file(file_path):
    
    hdu_list = fits.open(file_path)   # open the FITS file

    if len(hdu_list) != 1:
        raise Exception("The FITS file should contain only one HDU.")

    image_array = hdu_list[0].data    # "hdu.data" is a Numpy Array

    hdu_list.close()

    return image_array


def save_image(img, output_file_path):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.savefig(output_file_path)


def plot_image(img):
    """
    img should be a 2D numpy array.
    """
    fig = plt.figure(figsize=(8.0, 8.0))
    ax = fig.add_subplot(111)
    ax.imshow(img, interpolation='nearest', cmap=cm.gray)
    plt.show()


def main():

    # PARSE OPTIONS ###############################################################

    parser = argparse.ArgumentParser(description="MrTransform wrapper.")

    parser.add_argument("--number_of_scales", "-n", type=int, default=4, metavar="INTEGER",
                        help="number of scales used in the multiresolution transform (default: 4)")
    parser.add_argument("filearg", nargs=1, metavar="FILE",
                        help="the FITS file to process")

    args = parser.parse_args()

    number_of_scales = args.number_of_scales
    input_file_path = args.filearg[0]


    # READ THE INPUT FILE #########################################################

    input_img = get_image_array_from_fits_file(input_file_path)

    if input_img.ndim != 2:
        raise Exception("Unexpected error: the input FITS file should contain a 2D array.")


    # EXECUTE MR_TRANSFORM ########################################################

    # TODO: improve the following lines
    cmd = 'mr_transform -n{} "{}" out'.format(number_of_scales, input_file_path)
    os.system(cmd)

    # TODO: improve the following lines
    cmd = "mv out.mr {}".format(MR_OUTPUT_FILE_PATH)
    os.system(cmd)


    # READ THE MR_TRANSFORM OUTPUT FILE ###########################################

    output_imgs = get_image_array_from_fits_file(MR_OUTPUT_FILE_PATH)

    if output_imgs.ndim != 3:
        raise Exception("Unexpected error: the output FITS file should contain a 3D array.")

    tmp_img = input_img

    for img_index, img in enumerate(output_imgs):
        #plot_image(img)
        if 0 < img_index <= 2:
            tmp_img = tmp_img - img

    #print(tmp_img)
    plot_image(tmp_img)

if __name__ == "__main__":
    main()
