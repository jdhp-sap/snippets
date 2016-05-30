#!/bin/bash

for SIMTEL_FILE in "$@"
do
    echo "${SIMTEL_FILE}"

    ./list_events.py ${SIMTEL_FILE} | while read -r LINE
    do
        RESULTARRAY=($LINE)

        EVENTID=${RESULTARRAY[0]}
        TELID=${RESULTARRAY[1]}

        OUTPUT_FILE_NAME="${SIMTEL_FILE}_TEL${TELID}_EV${EVENTID}_CH0"
        echo "${OUTPUT_FILE_NAME}"

        #echo "TELID=${TELID} EVENTID=${EVENTID}"
        ./plot_events_image.py -q -o "${OUTPUT_FILE_NAME}.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./plot_events_photoelectron_image.py -q -o "${OUTPUT_FILE_NAME}_PE.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./plot_events_image_histogram.py -q -o "${OUTPUT_FILE_NAME}_HIST.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./plot_events_photoelectron_image_histogram.py -q -o "${OUTPUT_FILE_NAME}_PE_HIST.pdf" -t $TELID -e "$EVENTID ${SIMTEL_FILE}" 2> /dev/null
        ./event_photoelectron_image_to_json.py -o "${OUTPUT_FILE_NAME}_PE.json" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        ./event_image_to_json.py -o "${OUTPUT_FILE_NAME}.json" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
    done

done
