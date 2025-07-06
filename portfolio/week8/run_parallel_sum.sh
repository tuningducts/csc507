# Usage:  ./run_parallel_sum.sh <file1> <file2> <num_chunks>

set -euo pipefail

##############################################################################
# Args & validation
##############################################################################
if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <file1> <file2> <num_chunks>" >&2
    exit 1
fi

FILE1=$1
FILE2=$2
CHUNKS=$3

if ! [[ $CHUNKS =~ ^[0-9]+$ && $CHUNKS -gt 0 ]]; then
    echo "Error: <num_chunks> must be a positive integer." >&2
    exit 2
fi

##############################################################################
# Temporary workspace
##############################################################################
TMPDIR=$(mktemp -d -p "$(pwd)" sumchunks_XXXXXX)
cleanup() { rm -rf "$TMPDIR"; }
trap cleanup EXIT INT TERM


##############################################################################
# Split inputs into CHUNKS parts  
##############################################################################
WIDTH=${#CHUNKS}
(( WIDTH < 2 )) && WIDTH=2

echo "Splitting $FILE1 and $FILE2 into $CHUNKS chunks …"
split_start=$(date +%s)

split -d -n l/"$CHUNKS" --suffix-length="$WIDTH" "$FILE1" "$TMPDIR/f1_"
split -d -n l/"$CHUNKS" --suffix-length="$WIDTH" "$FILE2" "$TMPDIR/f2_"

split_end=$(date +%s)
echo "Split phase:   $((split_end - split_start)) seconds"
echo "------------------------------------------------------------"

##############################################################################
# Determine worker count
##############################################################################
CORES=$(nproc)
WORKERS=$(( CHUNKS < CORES ? CHUNKS : CORES ))
SEQ=$(seq -f "%0${WIDTH}g" 0 $((CHUNKS-1)))


##############################################################################
# Process chunks in parallel 
##############################################################################
CORES=$(nproc)
WORKERS=$(( CHUNKS < CORES ? CHUNKS : CORES ))
SEQ=$(seq -f "%0${WIDTH}g" 0 $((CHUNKS-1)))

echo "Launching $WORKERS worker(s) (CPU cores = $CORES, chunks = $CHUNKS)…"
proc_start=$(date +%s)

printf "%s\n" $SEQ | xargs -I{} -P"$WORKERS" \
  bash -c 'python3 sum_chunk.py "'"$TMPDIR"'/f1_{}" "'"$TMPDIR"'/f2_{}" "'"$TMPDIR"'/out_{}.txt"'

proc_end=$(date +%s)
echo "Process phase: $((proc_end - proc_start)) seconds"
echo "------------------------------------------------------------"
##############################################################################
# Combine results
##############################################################################
echo "Concatenating → totalfile.txt …"
cat $(printf "$TMPDIR/out_%0${WIDTH}g.txt " $SEQ) > totalfile.txt

echo "Done - Output saved as totalfile.txt — temp files cleaned."
