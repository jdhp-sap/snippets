#!/bin/bash

./list_common_events.py "$@" | while read -r LINE
do
    RESULTARRAY=($LINE)

    SIMTEL_FILE=${RESULTARRAY[0]}
    EVENTID=${RESULTARRAY[1]}
    TELID=${RESULTARRAY[2]}

    echo "FILE=${SIMTEL_FILE} TELID=${TELID} EVENTID=${EVENTID}"
    ./plot_events_image.py -q -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./plot_events_photoelectron_image.py -q -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./plot_events_image_histogram.py -q -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./plot_events_photoelectron_image_histogram.py -q -t $TELID -e "$EVENTID ${SIMTEL_FILE}" 2> /dev/null
    ./event_photoelectron_image_to_json.py -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./event_image_to_json.py -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
done
