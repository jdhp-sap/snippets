#!/bin/bash

INPUT_DIR=~/data/sim_008/

################################################################################

./plot_all_common_events.sh ${INPUT_DIR}/*cta-prod3-demo_desert-2150m-Paranal-n*.gz

mkdir default
mv *.pdf default/
mv *.json default/

################################################################################

./plot_all_common_events.sh ${INPUT_DIR}/*cta-prod3-demo_desert-2150m-Paranal-c*.gz

mkdir nonoise
mv *.pdf nonoise/
mv *.json nonoise/

################################################################################

./plot_all_common_events.sh ${INPUT_DIR}/*cta-prod3-demo_desert-2150m-Paranal-n*.gz

mkdir almost_nonoise
mv *.pdf almost_nonoise/
mv *.json almost_nonoise/

