#!/bin/bash
pip install nltk
pip install bs4
sudo ln -s ./invidx.py /usr/local/bin/invidx
sudo chmod 755 /usr/local/bin/index
sudo chmod u+x ./invidx.py
sudo chmod u+x ./Trie.py
sudo chmod u+x ./vecsearch.py
sudo chmod u+x ./printdict.py
