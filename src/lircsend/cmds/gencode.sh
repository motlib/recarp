# Convert output of mode2 to c code
#
# Removed first line from file. 

INPUT=$1
OUTPUT=${INPUT}.in

echo "Converting '${INPUT}' to '${OUTPUT}'."

cat ${INPUT} \
    | sed -r -e 's/^pulse (.*)$/LIRC_PULSE\(\1\),/' \
    | sed -r -e 's/^space (.*)$/LIRC_SPACE\(\1\),/' \
    | tail -n +2 > ${OUTPUT}
