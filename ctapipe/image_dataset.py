#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inspired by ctapipe/examples/read_hessio_single_tel.py
"""

import ctapipe
import ctapipe.visualization
from ctapipe.utils.datasets import get_example_simtelarray_file
from ctapipe.io.hessio import hessio_event_source

from matplotlib import pyplot as plt

# CONFIG ################################################################

filename = get_example_simtelarray_file()  # Get a simtel file from ctapipe-extra (it could be external data files)
tel_num = 1                                # The telescope number
max_events = 5
channel = 0

# GET EVENT #############################################################

# Source is a python generator.
# It contains ctapipe.core.Container instances ("event").
#
# Source contains few events (usually 0, 1 or 2)
source = hessio_event_source(filename, allowed_tels=[tel_num], max_events=max_events)

event_list = list(source)
event = event_list[0]

# INIT PLOT #############################################################

x, y = event.meta.pixel_pos[tel_num]
geom = ctapipe.io.CameraGeometry.guess(x, y)
disp = ctapipe.visualization.CameraDisplay(geom, title='CT%d' % tel_num)
disp.enable_pixel_picker()
disp.add_colorbar()

disp.axes.set_title('CT{:03d}, event {:010d}'.format(tel_num, event.dl0.event_id))

# DISPLAY TIME-VARYING EVENT ############################################

#data = event.dl0.tel[tel_num].adc_samples[channel]
#for ii in range(data.shape[1]):
#    disp.image = data[:, ii]
#    disp.set_limits_percent(70)
#    plt.savefig('CT{:03d}_EV{:010d}_S{:02d}.png'.format(tel_num, event.dl0.event_id, ii))

# DISPLAY INTEGRATED EVENT ##############################################

disp.image = event.dl0.tel[tel_num].adc_sums[channel]
disp.set_limits_percent(70)
plt.savefig('CT{:03d}_EV{:010d}.png'.format(tel_num, event.dl0.event_id))

# PLOT ##################################################################

plt.show()
