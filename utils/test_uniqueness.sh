#!/bin/bash

rm -f test_results
touch test_results

watch -n 1 "echo -n 'Total: ' ; cat test_results | wc -l ; echo -n 'Uniq:  ' ; sort test_results | uniq | wc -l" &

function cleanup {
    kill $!
}
trap cleanup EXIT

while true ; do
    echo 'This is a test' | nc termcat.io 9999 | cut -d '/' -f 5 >> test_results
    sleep 1
done
