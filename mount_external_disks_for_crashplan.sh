#!/bin/bash
lvchange -ay /dev/wdmp
lvchange -ay /dev/wde

# cd /dev/mapper && rm /tmp/in.txt
# for i in `ls -x1`; do blkid $i >> /tmp/in.txt; done

