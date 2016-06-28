#!/bin/bash

SIMTEL_FILE="$1"

if [ ! -f "${SIMTEL_FILE}" ]
then
    echo "USAGE:"
    echo "$0 SIMTEL_FILE"
    exit 1
fi

for TELID in $(seq 1 125)
do
    echo "$TELID"
    ./plot_telescope_pedestal.py -t $TELID -q "${SIMTEL_FILE}" 2> /dev/null
    ./plot_telescope_gain.py -t $TELID -q "${SIMTEL_FILE}" 2> /dev/null
done
