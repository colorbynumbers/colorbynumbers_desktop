#!/bin/sh
export PATH=~/anaconda3/bin:$PATH

if conda env list | grep -q 'cbn'; then
    echo "cbn exists"
else
    echo "cbn does not exists"
    conda env create -f environment.yml
fi

eval "$(conda shell.bash hook)"
conda activate cbn

cd src/
python ColorByNumber.py
