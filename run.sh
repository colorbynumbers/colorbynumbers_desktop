#!/bin/sh
if conda env list | grep -q 'cbn'; then
   source activate cbn
else
   conda env create -f environment.yml
   source activate cbn 
fi

cd src/
python ColorByNumber.py