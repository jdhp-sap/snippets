#!/bin/bash

for SIMTEL_FILE in "$@"
do
    echo "${SIMTEL_FILE}"

    ./list_events.py ${SIMTEL_FILE} | while read -r LINE
    do
        RESULTARRAY=($LINE)
        EVENTID=${RESULTARRAY[0]}
        TELID=${RESULTARRAY[1]}

        echo "TELID=${TELID} EVENTID=${EVENTID}"
        ./plot_events_image.py -q -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./plot_events_photoelectron_image.py -q -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./plot_events_image_histogram.py -q -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./plot_events_photoelectron_image_histogram.py -q -t $TELID -e "$EVENTID ${SIMTEL_FILE}" 2> /dev/null
        ./event_photoelectron_image_to_json.py -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./event_image_to_json.py -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    done

done
