#!/bin/bash

./list_common_events.py "$@" | while read -r LINE
do
    RESULTARRAY=($LINE)

    SIMTEL_FILE=${RESULTARRAY[0]}
    EVENTID=${RESULTARRAY[1]}
    TELID=${RESULTARRAY[2]}

    OUTPUT_FILE_NAME="${SIMTEL_FILE}_TEL${TELID}_EV${EVENTID}_CH0"
    echo "${OUTPUT_FILE_NAME}"

    #echo "FILE=${SIMTEL_FILE} TELID=${TELID} EVENTID=${EVENTID}"
    ./plot_events_image.py -q -o "${OUTPUT_FILE_NAME}.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./plot_events_photoelectron_image.py -q -o "${OUTPUT_FILE_NAME}_PE.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./plot_events_image_histogram.py -q -o "${OUTPUT_FILE_NAME}_HIST.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./plot_events_photoelectron_image_histogram.py -q -o "${OUTPUT_FILE_NAME}_PE_HIST.pdf" -t $TELID -e "$EVENTID ${SIMTEL_FILE}" 2> /dev/null
    ./event_photoelectron_image_to_json.py -o "${OUTPUT_FILE_NAME}_PE.json" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    ./event_image_to_json.py -o "${OUTPUT_FILE_NAME}.json" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
done
