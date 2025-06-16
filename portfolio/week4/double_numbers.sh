if [ $# -eq 0 ]; then
    echo "No arguments provided."
    exit 1
fi

file=$1

while read -r number
do

  (( number *= 2 ))

  echo $number >> newfile1.txt

done < $file
