#! usr/bin/bash

python divide.py
echo "info_gain:"
python model.py info_gain
python predict.py
echo "gain_ratio:"
python model.py gain_ratio
python predict.py
echo "gini_index:"
python model.py gini_index
python predict.py