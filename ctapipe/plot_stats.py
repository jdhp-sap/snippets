#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make statistics on simtel images (stored in JSON files).
"""

import ctapipe
import ctapipe.visualization
from ctapipe.io.hessio import hessio_event_source

import argparse
import json
import matplotlib.pyplot as plt
import numpy as np

def fetch_images(json_file_path_list):

    image_list = []

    # For each json file...
    for json_file_path in json_file_path_list:
        print(json_file_path)
        with open(json_file_path, "r") as fd:
            image = json.load(fd)
            image_list.append(image)

    return image_list


if __name__ == '__main__':

    # PARSE OPTIONS ###########################################################

    parser = argparse.ArgumentParser(description="Make statistics on simtel images (stored in JSON files).")

    parser.add_argument("fileargs", nargs="+", metavar="FILE",
                        help="The JSON files to process")

    args = parser.parse_args()
    json_file_path_list = args.fileargs

    # FETCH IMAGES ############################################################

    image_list = fetch_images(json_file_path_list)
    image_array = np.array(image_list)

    # MAKE STATISTICS #########################################################

    img_min = np.min(image_array, axis=0)
    img_max = np.max(image_array, axis=0)
    img_mean = np.mean(image_array, axis=0)
    img_median = np.median(image_array, axis=0)
    img_std = np.std(image_array, axis=0)

    # Get pixels where variance != 0 (i.e. where min != max)
    nonzero_pixels_mask = (img_min != img_max)
    nonzero_pixels_index = np.nonzero(nonzero_pixels_mask)[0]
    nonzero_image_array = image_array[:, nonzero_pixels_index]

    print("NON-ZERO IMAGES:", nonzero_image_array)
    print("NON-ZERO IMAGE MIN:", img_min[nonzero_pixels_index])
    print("NON-ZERO IMAGE MAX:", img_max[nonzero_pixels_index])
    print("NON-ZERO IMAGE MEAN:", img_mean[nonzero_pixels_index])
    print("NON-ZERO IMAGE MEDIAN:", img_median[nonzero_pixels_index])
    print("NON-ZERO IMAGE STD:", img_std[nonzero_pixels_index])

    # PLOT STATISTICS #########################################################

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(14, 8))

    #x = np.arange(len(image_list[0]))
    x = np.arange(len(nonzero_pixels_index))

    ax1.bar(x, img_std[nonzero_pixels_index], color='b')
    ax1.set_title(r"Standard deviation of pixels (only show pixels with $\sigma > 0$)")

    meanpointprops = dict(marker='*', markeredgecolor='black', markerfacecolor='firebrick')
    ax2.boxplot(nonzero_image_array, meanprops=meanpointprops, meanline=False, showmeans=True)

    # Save file and plot ########

    #plt.savefig("stats.pdf")
    plt.show()

    # PLOT MEAN IMAGE #########################################################

