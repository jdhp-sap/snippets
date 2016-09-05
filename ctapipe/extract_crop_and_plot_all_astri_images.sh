#!/bin/bash

echo "****************************************************************************************"
echo "* This script is deprecated, use ''extract_crop_and_plot_all_astri_images.py'' instead *"
echo "****************************************************************************************"

for SIMTEL_FILE in "$@"
do
    echo "${SIMTEL_FILE}"

    ./list_events.py ${SIMTEL_FILE} | while read -r LINE
    do
        RESULTARRAY=($LINE)

        EVENTID=${RESULTARRAY[0]}
        TELID=${RESULTARRAY[1]}

        if [ $TELID -ge 1 -a $TELID -le 33 ]
        then
            OUTPUT_FILE_NAME="${SIMTEL_FILE}_TEL${TELID}_EV${EVENTID}_CH0"
            echo "${OUTPUT_FILE_NAME}"

            #echo "TELID=${TELID} EVENTID=${EVENTID}"
            ./extract_and_crop_simtel_images.py -o "${OUTPUT_FILE_NAME}.fits" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
            #./plot_events_image.py -q -o "${OUTPUT_FILE_NAME}.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
            #./plot_events_calibrated_image.py -q -o "${OUTPUT_FILE_NAME}.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
            #./plot_events_photoelectron_image.py -q -o "${OUTPUT_FILE_NAME}_PE.pdf" -t $TELID -e $EVENTID "${SIMTEL_FILE}" 2> /dev/null
        fi
    done

done
