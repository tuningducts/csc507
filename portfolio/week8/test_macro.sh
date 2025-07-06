if (( $(head -n1 hugefile1.txt) + $(head -n1 hugefile2.txt) == $(head -n1 totalfile.txt) )); then
    echo "first-line sum matches"
else
    echo " first-line sum mismatch"
fi
    if (( $(tail -n1 hugefile1.txt) + $(tail -n1 hugefile2.txt) == $(tail -n1 totalfile.txt) )); then
    echo "last-line sum matches"
else
    echo " last-line sum mismatch"
fi
