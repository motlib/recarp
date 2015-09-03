# Convert output of mode2 to c code
#
# Removed first line from file. 

INPUT=$1
OUTPUT=${INPUT}.in

echo "Converting '${INPUT}' to '${OUTPUT}'."

cat ${INPUT} | head -n 1 | grep pulse || echo "WARNING: Sequence does not start with a pulse."

cat ${INPUT} \
    | sed -r -e 's/^pulse (.*)$/\1\,/' \
    | sed -r -e 's/^space (.*)$/\1\,/' > ${OUTPUT}

